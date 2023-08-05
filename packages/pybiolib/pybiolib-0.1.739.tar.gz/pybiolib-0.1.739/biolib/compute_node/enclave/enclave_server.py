import socket
import json
import base64
import io
import os
import subprocess
import logging
import docker
import tarfile
import socket
import zipfile
from biolib_binary_format.ModuleInput import ModuleInput
from biolib_binary_format.ModuleOutput import ModuleOutput
from BiolibDockerClient import BiolibDockerClient
from asyncio import IncompleteReadError
from NsmUtil import NSMUtil
import enclave_config
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def main():
    biolib_logger = logging.getLogger('biolib')
    logging.basicConfig(level=logging.ERROR)

    nsm_util = NSMUtil()
    biolib_docker_client = BiolibDockerClient()

    # Shared state
    aes_key_buffer = b''
    module_input = {}
    try:
        client_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        cid = socket.VMADDR_CID_ANY
        client_socket.bind((cid, enclave_config.CLIENT_PORT))
        client_socket.listen()

        while True:
            connection, addr = client_socket.accept()

            while True:

                request = json.loads(connection.recv(enclave_config.DEFAULT_BUFFER_SIZE).decode())

                if request['route'] == 'do_attestation':
                    attestation_doc = nsm_util.get_attestation_doc()
                    connection.send(base64.b64encode(attestation_doc))

                elif request['route'] == 'load_image':
                    send_ok(connection)
                    image_bytes = readexactly(connection, request['size'])
                    with open('/tmp/image.tar', 'wb') as f:
                        f.write(image_bytes)
                    # Use the docker CLI as docker-py does not seem to import image metadata when loading
                    subprocess.run(['docker','image', 'load', '-i', '/tmp/image.tar'], capture_output=True, text=True)

                elif request['route'] == 'load_data':
                    send_ok(connection)
                    encrypted_data = readexactly(connection, request['size'])
                    aes_key_buffer, nonce = get_keys(request['keys'], nsm_util)
                    cipher = AES.new(aes_key_buffer, AES.MODE_GCM, nonce=nonce)
                    serialized_data = cipher.decrypt(encrypted_data)
                    module_input = ModuleInput(serialized_data).deserialize()

                elif request['route'] == 'start_compute':
                    biolib_logger.debug(f'Command: {request["command"]} {" ".join(module_input["arguments"])}')
                    biolib_docker_client.create_container(
                                image=request['image'], 
                                command=f'{request["command"]} {" ".join(module_input["arguments"])}', 
                                working_dir=request['working_dir']
                    )

                    # Also pass arguments so we can parse $ variables when mapping later
                    biolib_docker_client.set_mappings(
                                request['input_mappings'], 
                                request['source_mappings'], 
                                request['output_mappings'], 
                                module_input['arguments']
                            )

                    if request['runtime_zip_size']:
                        send_ok(connection)
                        runtime_zip_data = readexactly(connection, request['runtime_zip_size'])
                        biolib_docker_client.map_and_copy_runtime_files_to_container(runtime_zip_data)

                    biolib_docker_client.map_and_copy_input_files_to_container(module_input['files'])

                    stdout, stderr, exit_code, mapped_output_files = biolib_docker_client.run_container()

                    module_output = ModuleOutput().serialize(stdout, stderr, exit_code, mapped_output_files)
                    encrypted_result, nonce = encrypt_result(module_output, aes_key_buffer)

                    result_response = json.dumps({'size':len(encrypted_result), 'keys':{'iv': nonce.hex()}})
                    connection.send(result_response.encode())
                    check_ok(connection)
                    connection.sendall(encrypted_result)
                    biolib_logger.debug("Sent result")
                    break
    
            connection.close()
            break

    except Exception as e:
        biolib_logger.error(e)
        # Send 'error' string to force an exception to be thrown in the parent client 
        connection.send('error'.encode())
        connection.close()
 
def readexactly(sock: socket.socket, num_bytes: int) -> bytes:
    buf = bytearray(num_bytes)
    pos = 0
    while pos < num_bytes:
        n = sock.recv_into(memoryview(buf)[pos:])
        if n == 0:
            raise IncompleteReadError(bytes(buf[:pos]), num_bytes)
        pos += n

    # Send OK to parent so it can send the next request
    send_ok(sock)

    return bytes(buf)


def send_ok(c):
    c.send("OK".encode())


def get_keys(keys, nsm_util):
    nonce = bytes.fromhex(keys['iv'])
    # Decrypt the aes_key_buffer
    aes_key_buffer = nsm_util.decrypt(bytes.fromhex(keys['encrypted_aes_key_buffer']))
    return (aes_key_buffer, nonce)


def encrypt_result(result, aes_key_buffer):
    nonce = get_random_bytes(12)
    cipher = AES.new(aes_key_buffer, AES.MODE_GCM, nonce=nonce)
    encrypted_result, tag = cipher.encrypt_and_digest(result)
    return (encrypted_result + tag, nonce)


def check_ok(connection):
    if connection.recv(enclave_config.OK_BUFFER_SIZE).decode() != 'OK':
        raise Exception('OK check failed')


if __name__ == '__main__':
    main()
