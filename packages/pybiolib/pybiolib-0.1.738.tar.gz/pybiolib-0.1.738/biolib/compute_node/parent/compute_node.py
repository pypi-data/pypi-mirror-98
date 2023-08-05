from flask import Flask, request, Response
from flask.json import jsonify
from flask_cors import CORS, cross_origin
import requests
import threading
import json
import os
import logging
import datetime
import gunicorn.app.base
# Needed to call guniorn from Python (Results in import errors if removed)
from gunicorn import glogging
from gunicorn.workers import sync

import subprocess
from socket import gethostname, gethostbyname
from biolib.compute_node.parent.parent_client import run_client
from biolib.compute_node.parent import parent_config

app = Flask(__name__)
CORS(app)
biolib_logger = logging.getLogger('biolib')

# Global variables
locks = {lock_name: threading.Lock() for lock_name in ['attestation', 'cloud_job_state', 'input_data', 'result']}
cloud_job = {
    'status_and_progress': {'message': 'Starting', 'progress': 0},
    'encrypted_result': '',
    'encrypted_input_data': '',
    'error': '',
    'eif_path': '',
    'input_keys': {},
    'result_keys': {},
    'cloud_job_state': {},
    'attestation_document_b64': ''
}

dev_mode = True if os.environ.get('COMPUTE_NODE_ENV', '') == 'dev' else False

if dev_mode:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)

def shutdown_after_response():
    biolib_logger.debug("Shutting down...")
    if not dev_mode:
        subprocess.run(['sudo', 'shutdown', 'now'])


@app.before_first_request
def initialize_parent_client():
    # Immediately acquire all locks to make sure blocking works correctly down the line
    biolib_logger.debug("Started Compute Node and locking locks")
    for lock in locks.values():
        lock.acquire()

    threading.Thread(target=run_client, args=(locks, cloud_job)).start()


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/save_cloud_job/', methods=['POST'])
def save_cloud_job():
    global cloud_job
    cloud_job['cloud_job_state'] = request.get_json()
    locks['cloud_job_state'].release()

    # Start self destruct timer
    if not dev_mode:
        subprocess.Popen(['sudo', 'shutdown', f'+{parent_config.COMPUTE_NODE_RUNNING_JOB_SHUTDOWN_TIME_MINUTES}'])
    return "", 201


@app.route('/get_attestation_document/')
def get_attestation_document():
    global cloud_job
    return jsonify({'attestation_document_base64': cloud_job['attestation_document_b64']}), 201


@app.route('/start_cloud_job/', methods=['POST'])
def start_cloud_job():
    global cloud_job
    cloud_job['encrypted_input_data'] = request.data
    cloud_job['input_keys'] = json.loads(request.headers['Keys'])
    locks['input_data'].release()
    return "", 201


@app.route('/status/')
def status():
    global cloud_job
    if cloud_job['error']:
        error_response = app.response_class(response=cloud_job['error'],
                                status=500,
                                mimetype='application/json')
        error_response.call_on_close(shutdown_after_response)
        return error_response

    return jsonify(cloud_job['status_and_progress']), 200


@app.route('/result/')
@cross_origin(expose_headers=['Keys'])
def result():
    global cloud_job
    response = Response(cloud_job['encrypted_result'])
    response.headers['Keys'] = json.dumps(cloud_job['result_keys'])
    response.call_on_close(shutdown_after_response)
    return response


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    # Needed to load the options
    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    # Needed to overload base class
    def load(self):
        return self.application


def start_flask_compute_node(port, eif_path=None):
    global cloud_job

    # Report availability and set general shutdown timer
    if not dev_mode and eif_path:
        subprocess.Popen(["sudo", "shutdown", f"+{parent_config.COMPUTE_NODE_SHUTDOWN_TIME_MINUTES}"])

        try:
            biolib_logger.debug(f'.bashrc at the start of Compute Node: {open("/home/ec2-user/.bashrc", "r").read()}')
            node_public_id = os.getenv('BIOLIB_COMPUTE_NODE_PUBLIC_ID')
            auth_token = os.getenv('BIOLIB_COMPUTE_NODE_AUTH_TOKEN')
            biolib_host = os.getenv('BIOLIB_HOST')
            ip_address = gethostbyname(gethostname())
            data = {'public_id':node_public_id, 'auth_token':auth_token, 'ip_address':ip_address}
            biolib_logger.debug(f'Registering with {data} to host {biolib_host}')
            biolib_logger.debug(f'Registering at {datetime.datetime.now()}')
            r = requests.post(f'https://{biolib_host}/api/jobs/report_available/', json=json.dumps(data))
            if r.status_code != 200:
                raise Exception("Non 200 error code")

        except Exception as e:
            biolib_logger.error(f'Could not self register because of: {e}')
            if not dev_mode:
                subprocess.run(['sudo', 'shutdown', 'now'])
            biolib_logger.debug("Self destructing")


    options = {
        'bind': f'0.0.0.0:{port}',
        'workers': 1,
    }

    if eif_path:
        cloud_job['eif_path'] = eif_path

    StandaloneApplication(app, options).run()
