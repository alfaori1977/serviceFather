from flask import Flask, request, jsonify
from dotenv import load_dotenv
import subprocess
import os

import threading
import time

load_dotenv()  # take environment variables from .env.
app = Flask(__name__)
fileDir = os.path.dirname(__file__)
servicesDir = os.path.join(fileDir, '../services')
print(f"servicesDir: {servicesDir}")

PORT = os.environ.get("SERVICE_FATHER_PORT", 16000)
EXPECTED_TOKEN_ID = os.environ.get("SERVICE_FATHER_TOKEN_ID", "")
REPORT_IP = os.environ.get("SERVICE_FATHER_MGR_REPORT_IP", None)


def getErrorJson(service, action, completedProcess):
    # http 500: internal server error
    err = {'service': service,
           'action': action,
           'message': f"Error while running script '{action}.sh' for service '{service}'.",
           'stderr': completedProcess.stderr.decode('utf-8'),
           'stdout': completedProcess.stdout.decode('utf-8'),
           'returncode': completedProcess.returncode}

    return jsonify(err)


def getResponseJson(service, action, completedProcess):
    rsp = {'service': service,
           'action': action,
           'message': f"Action '{action}' performed for service '{service}'.",
           'stderr': completedProcess.stderr.decode('utf-8'),
           'stdout': completedProcess.stdout.decode('utf-8'),
           'returncode': completedProcess.returncode}
    return jsonify(rsp)


def enableService(service_name):
    with open(f'{servicesDir}/{service_name}/enabled', 'w') as f:
        f.write('')
    return


def disableService(service_name):
    if os.path.isfile(f'{servicesDir}/{service_name}/enabled'):
        os.remove(f'{servicesDir}/{service_name}/enabled')
    return


@app.route('/api', methods=['POST'])
def perform_post():
    data = request.json
    service_name = data.get('serviceName')
    action = data.get('action')
    token_id = data.get('token', None)
    action = action.lower()

    if not service_name or not action or not token_id:
        # http 400: bad request
        return jsonify({'returncode': 400, 'message': 'Service name, action, and tokenId are required.'}), 400

    if token_id != EXPECTED_TOKEN_ID:
        # http 401: unauthorized
        return jsonify({'returncode': 403, 'message': 'Incorrect tokenId. Access denied.'}), 401

    if action == 'enable':
        print(f"Enabling service '{service_name}'")
        enableService(service_name)
        return jsonify({'returncode': 200, 'message': f"Service '{service_name}' enabled."}), 200
    elif action == 'disable':
        disableService(service_name)
        return jsonify({'returncode': 200, 'message': f"Service '{service_name}' disabled."}), 200

    script_path = f'{servicesDir}/{service_name}/{action}.sh'
    if not os.path.isfile(script_path):
        return jsonify({'returncode': 404, 'message': f"Script '{action}.sh' not found for service '{service_name}'."}), 404

    isEnabled = os.path.isfile(f'{servicesDir}/{service_name}/enabled')
    if not isEnabled:
        return jsonify({'returncode': 500, 'message': f"Service '{service_name}' is disabled."}), 500

    completedProcess = subprocess.run(
        ['bash', script_path], capture_output=True)
    if completedProcess.returncode != 0:
        # http 500: internal server error
        return getErrorJson(service_name, action, completedProcess), 500
    # http 200: ok
    return getResponseJson(service_name, action, completedProcess), 200

# https://localhost:26000/api/services
# https://localhost:26000/api/services?kind=enabled
# https://localhost:26000/api/services?kind=disabled


@app.route('/api/services', methods=['GET'])
def get_services():
    kind = request.args.get("kind", "all")

    services = os.listdir(servicesDir)
    outServices = []
    for service in services:
        enabled = False
        if os.path.isfile(f'{servicesDir}/{service}/enabled'):
            enabled = True
        outServices.append({"service": service, "enabled": enabled})

    if (kind == "enabled"):
        outServices = list(
            filter(lambda service: service["enabled"], outServices))
    elif (kind == "disabled"):
        outServices = list(
            filter(lambda service: not service["enabled"], outServices))

    return jsonify(outServices), 200


"""

def reportStatus():
    url = f'http://{REPORT_IP}/get_my_ip'
    ip = request.get(url).json()['ip']
    print(f"Reporting status to {REPORT_IP} from {ip}")


def reportStatusThread():
    while True:
        reportStatus()
        time.sleep(5)


def startReportStatusThread():
    if REPORT_IP is None:
        return

    x = threading.Thread(target=reportStatusThread, args=())
    x.start()

"""
if __name__ == '__main__':
    # startReportStatusThread()
    app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=PORT)
