import sys
import socket
import json
import subprocess
import base64
import os
import threading
import io
import random
import docker
import requests
import shlex
import string
import zipfile
import logging
import tarfile
import shutil
import os
import time
import boto3
from biolib.compute_node.parent import parent_config
from asyncio import IncompleteReadError


from time import sleep

class BiolibException(Exception):
    pass

def run_client(locks, cloud_job):        
    try:
        s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)

        locks['cloud_job_state'].acquire()
        log_status(message='Saving module state', progress=5, cloud_job=cloud_job)
        cloud_job_state = cloud_job['cloud_job_state']
        module = cloud_job_state['module']

        log_status(message='Pulling images', progress=10, cloud_job=cloud_job)
        image_bytes, image_name = pull_image(s, module['image_uri'])

        log_status(message='Starting encrypted enclave', progress=20, cloud_job=cloud_job)
        start_and_connect_to_enclave(s, cloud_job)

        log_status(message='Sending images to enclave', progress=35, cloud_job=cloud_job)
        send_image_data_to_enclave(s, image_bytes)

        log_status(message='Creating attestation document', progress=50, cloud_job=cloud_job)
        send_request(s, {'route': 'do_attestation'})
        cloud_job['attestation_document_b64'] = s.recv(parent_config.ATTESTATION_DOC_BUFFER_SIZE).decode()
        locks['attestation'].release()
        log_status(message='Attestation document ready', progress=55, cloud_job=cloud_job)

        locks['input_data'].acquire()
        log_status(message='Sending the encrypted data to Enclave', progress=60, cloud_job=cloud_job)
        send_input_data_to_enclave(s, cloud_job['encrypted_input_data'], keys=cloud_job['input_keys'])
        locks['input_data'].release()
        
        runtime_zip = cloud_job_state.get('runtime_zip')
        encrypted_result, result_keys = run_docker_application_in_enclave(s, image_name, module, runtime_zip, cloud_job)
        cloud_job['encrypted_result'] = encrypted_result
        cloud_job['result_keys'] = result_keys
        locks['result'].release()
        log_status(message='Result is ready', progress=100, cloud_job=cloud_job)
    
    except BiolibException as bl_error:
        cloud_job['error'] = json.dumps({'detail': str(bl_error)})

    except Exception as e:
        log_error(e)
        cloud_job['error'] = json.dumps({'detail': "The Cloud Job was not completed. An unknown error occured"})

    s.close()

def start_and_connect_to_enclave(s, cloud_job):
    # Start the enclave
    subprocess.run(shlex.split(f"nitro-cli run-enclave --cpu-count 2 --memory 8192 --eif-path {cloud_job['eif_path']}"))

    # Get CID of running enclave from nitro cli
    log_status(message='Waiting for enclave to start', progress=25, cloud_job=cloud_job)

    enclave_cid = None
    while True:
        if isinstance(enclave_cid, str) and enclave_cid.isnumeric():
            break
        enclave_cid = subprocess.run(
            'nitro-cli describe-enclaves | jq -r ".[0].EnclaveCID"', 
            check=True, 
            stdout=subprocess.PIPE, 
            universal_newlines=True, 
            shell=True
        ).stdout.strip()
        sleep(0.1)

    # Sleep 4.5 seconds to let enclave start its socket correctly. Things break if we do not include this.
    sleep(4.5)
    log_status(message='Connecting to enclave', progress=30, cloud_job=cloud_job)
    
    # Retry until enclave is up and running
    retries = 0
    while s.connect_ex((int(enclave_cid), parent_config.ENCLAVE_PORT)) != 0:
        if retries > 20:
            raise BiolibException("Could not establish connection to enclave")
        retries += 1
        sleep(1)

def pull_image(s, repo_uri):
    try:
        docker_client = docker.from_env()
        
        # Log in to ECR
        client = boto3.client('ecr', region_name='eu-west-1')
        token = client.get_authorization_token(registryIds=[parent_config.BIOLIB_AWS_ECR_ID])
        password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')[-1]
        docker_client.login(username="AWS", password=password, registry=parent_config.BIOLIB_AWS_ECR_URL)    
    
    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to login to Biolib Container Registry")
    
    try:
        # Download image from ECR
        # Temporary hack to let scloud app depend on our tflite executor
        if os.environ.get("BIOLIB_EXECUTOR_APP_VERSION_ID") in repo_uri:
            repo_uri = os.environ.get("BIOLIB_SCLOUD_REPO")
        image = docker_client.images.pull(f'{parent_config.BIOLIB_AWS_ECR_URL}/{repo_uri}')

        # Send image to enclave
        image_bytes = io.BytesIO()
        for chunk in image.save(named=True):
            image_bytes.write(chunk)

    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to pull docker image from Biolib Container")

    return (image_bytes, repo_uri)


def send_image_data_to_enclave(s, image_bytes):
    try:
        send_request(s, {'route': "load_image", 'size': len(image_bytes.getbuffer())}, check=True)
        send_bytes_to_enclave(s, image_bytes.getbuffer(), check=True)
    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to send image to enclave")


def send_input_data_to_enclave(s, input_data, keys):
    try:
        send_request(s, {'route': "load_data", 'size': len(input_data), 'keys': keys}, check=True)
        send_bytes_to_enclave(s, input_data, check=True)
    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to send input data to enclave")

def run_docker_application_in_enclave(s, image_name, module, runtime_zip, cloud_job):
    runtime_zip_data = None
    runtime_zip_size = None
    if runtime_zip:
        log_status(message='Downloading source files', progress=70, cloud_job=cloud_job)
        r = requests.get(runtime_zip)
        if not r.status_code == 200:
            raise BiolibException("Failed to download runtime zip")
        runtime_zip_data = r.content
        runtime_zip_size = len(r.content)

    log_status(message='Starting computation in enclave', progress=75, cloud_job=cloud_job)
    
    try:
        send_request(s, {
                'route': "start_compute", 
                'image': f'{parent_config.BIOLIB_AWS_ECR_URL}/{image_name}', 
                'working_dir': module.get('working_directory'),
                'input_mappings': module.get('input_files_mappings', []), 
                'source_mappings': module.get('source_files_mappings', []),
                'output_mappings': module.get('output_files_mappings', []),
                'module_name': module.get('name'),
                'command': module.get('command', ''),
                'runtime_zip_size': runtime_zip_size
            })

    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to send compute request to enclave")


    if runtime_zip_data:
        try:
            check_ok(s)
            send_bytes_to_enclave(s, runtime_zip_data, check=True)
        except Exception as e:
            log_error(e)
            raise BiolibException("Failed to send runtime zip to enclave")

    log_status(message='Computing...', progress=80, cloud_job=cloud_job)

    try:
        result_request = json.loads(s.recv(parent_config.DEFAULT_BUFFER_SIZE).decode())
        s.send("OK".encode())
        log_status(message='Getting result from enclave...', progress=95, cloud_job=cloud_job)
        encrypted_result = readexactly(s, result_request['size'])
    except Exception as e:
        log_error(e)
        raise BiolibException("Failed to run the container in the enclave")
    
    return (encrypted_result, result_request['keys'])


def check_ok(c):
    if c.recv(parent_config.OK_BUFFER_SIZE).decode() != 'OK':
        raise Exception('OK failed')


def send_request(s, request, check=False):
    s.send(json.dumps(request).encode())
    if check:
        check_ok(s)


def send_bytes_to_enclave(s, byte_obj, check=False):
    s.sendall(byte_obj)
    if check:
        check_ok(s)


def readexactly(sock: socket.socket, num_bytes: int) -> bytes:
    buf = bytearray(num_bytes)
    pos = 0
    while pos < num_bytes:
        n = sock.recv_into(memoryview(buf)[pos:])
        if n == 0:
            raise IncompleteReadError(bytes(buf[:pos]), num_bytes)
        pos += n
    return bytes(buf)


def log_status(message, progress, cloud_job):
    biolib_logger = logging.getLogger('biolib')
    biolib_logger.debug(message)
    cloud_job['status_and_progress'] = {'message': message, 'progress': progress}


def log_error(error_message):
    biolib_logger = logging.getLogger('biolib')
    biolib_logger.error(error_message)
