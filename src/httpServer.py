
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import subprocess
import os

import requests
import threading
import time
import json
import platform
import datetime

load_dotenv()  # take environment variables from .env.
app = Flask(__name__)
fileDir = os.path.dirname(__file__)
servicesDir = os.path.join(fileDir, '../services')
print(f"servicesDir: {servicesDir}")

PORT = os.environ.get("SERVICE_FATHER_PORT", 16000)
EXPECTED_TOKEN_ID = os.environ.get("SERVICE_FATHER_TOKEN_ID", "")
REPORT_IP = os.environ.get("SERVICE_FATHER_MGR_REPORT_IP", None)
REPORT_INTERVAL_SECS = os.environ.get("SERVICE_FATHER_MGR_REPORT_INTERVAL", 2)
HOSTNAME = platform.node()
MAX_KAP_OFFSET = int(os.environ.get("MAX_SERVICES_KAP_OFFSET_SECONDS", 10))

serviceStatus = {}

def getErrorJson(service, action, completedProcess):
    # http 500: internal server error
    err = {'service': service,
           'action': action,
           'message': f"Error while running script '{action}.sh' for service '{service}'.",
           'stderr': completedProcess.stderr.decode('utf-8'),
           'stdout': completedProcess.stdout.decode('utf-8'),
           'returncode': completedProcess.returncode}

    return err


def getResponseJson(service, action, completedProcess):
    rsp = {'service': service,
           'action': action,
           'message': f"Action '{action}' performed for service '{service}'.",
           'stderr': completedProcess.stderr.decode('utf-8'),
           'stdout': completedProcess.stdout.decode('utf-8'),
           'returncode': completedProcess.returncode}
    return rsp


def enableService(service_name):
    with open(f'{servicesDir}/{service_name}/enabled', 'w') as f:
        f.write('')
    return


def disableService(service_name):
    if os.path.isfile(f'{servicesDir}/{service_name}/enabled'):
        os.remove(f'{servicesDir}/{service_name}/enabled')
    return


def getPostResponse(json):
    # print(f"Performing post request: {json}")
    data = json
    service_name = data.get('serviceName')
    action = data.get('action')
    token_id = data.get('token', None)
    action = action.lower()

    if not service_name or not action or not token_id:
        # http 400: bad request
        return {'returncode': 400, 'message': 'Service name, action, and tokenId are required.'}, 400

    if token_id != EXPECTED_TOKEN_ID:
        # http 401: unauthorized
        return {'returncode': 403, 'message': 'Incorrect tokenId. Access denied.'}, 401

    if action == 'enable':
        # print(f"Enabling service '{service_name}'")
        enableService(service_name)
        return {'returncode': 200, 'message': f"Service '{service_name}' enabled."}, 200
    elif action == 'disable':
        disableService(service_name)
        return {'returncode': 200, 'message': f"Service '{service_name}' disabled."}, 200

    script_path = f'{servicesDir}/{service_name}/{action}.sh'
    if not os.path.isfile(script_path):
        return {'returncode': 404, 'message': f"Script '{action}.sh' not found for service '{service_name}'."}, 404

    isEnabled = os.path.isfile(f'{servicesDir}/{service_name}/enabled')
    if not isEnabled:
        return {'returncode': 500, 'message': f"Service '{service_name}' is disabled."}, 500

    # print(f"Running script '{action}.sh' for service '{service_name}'")
    completedProcess = subprocess.run(
        ['bash', script_path], capture_output=True)
    if completedProcess.returncode != 0:
        # http 500: internal server error
        return getErrorJson(service_name, action, completedProcess), 500
    # http 200: okq
    return getResponseJson(service_name, action, completedProcess), 200


@app.route('/api', methods=['POST'])
def perform_post():
    json, http_code = getPostResponse(request.json)
    print("forcing reportStatus")
    reportStatus()
    return jsonify(json), http_code

@app.route('/api/kap', methods=['POST'])
def perform_kap():
    data = request.json
    serviceName = data.get('serviceName')
    status = data.get('status','')
    kapTime = datetime.datetime.now()
    print(f"KAP: {serviceName} {status} {kapTime}")
    serviceStatus[serviceName] = {'status': status, 'time': kapTime}    
    return jsonify({'returncode': 200, 'message': f"KAP: {serviceName} {status} {kapTime}"}), 200

def calculateKapStatus():
    for serviceName in serviceStatus:
        kapTime = serviceStatus[serviceName]['time']
        now = datetime.datetime.now()
        delta = now - kapTime
        serviceStatus[serviceName]['kapDelta'] = delta.seconds
        serviceStatus[serviceName]['kapOk'] = delta.seconds <= MAX_KAP_OFFSET

@app.route('/api/kap', methods=['GET'])
def get_kap():
    serviceName = request.args.get("serviceName", None)
    calculateKapStatus()
    if serviceName is None:
        return jsonify(serviceStatus), 200
    else:
        print(f"serviceName: {serviceName}")
        if serviceName not in serviceStatus:
            return jsonify({'kapOk': False, 'status': "unknown", "time" : "unknown"}), 200
        return jsonify(serviceStatus[serviceName]), 200



# https://localhost:26000/api/services
# https://localhost:26000/api/services?kind=enabled
# https://localhost:26000/api/services?kind=disabled


def getServices(kind='all'):
    # print(f"Getting services of kind '{kind}'")
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
    return outServices


@ app.route('/api/services', methods=['GET'])
def get_services():
    kind = request.args.get("kind", "all")
    outServices = getServices(kind)
    return jsonify(outServices), 200


def reportStatus():
    if REPORT_IP is None:
        return
    # url = f'http://{REPORT_IP}/get_my_ip'
    # ip = requests.get(url).json()['ip']
    # print(f"Reporting status to {REPORT_IP} from {ip}", flush=True)
    allServices = getServices()
    globalStatus = []
    for service in allServices:
        serviceName = service['service']
        enabled = service['enabled']
        statusRequest = {"serviceName": serviceName,
                         "action": "status",
                         "token": EXPECTED_TOKEN_ID}
        statusRequest, code = getPostResponse(statusRequest)
        # print(f"service: {service}")
        # print(f"statusRequest: {statusRequest}")
        srvStatus = {
            'hostname': HOSTNAME,
            'port': PORT,
            'service': serviceName,
            'enabled': enabled,
            'statusMessage': statusRequest['message'],
            'returncode': statusRequest['returncode']
        }
        globalStatus.append(srvStatus)

    statusJson = json.dumps(globalStatus)

    # print(f"globalStatus: {statusJson}")
    try:
        response = requests.post(f'http://{REPORT_IP}/status',
                                 json=globalStatus, verify=False, timeout=1)
        # print(f"response: {response}")
    except Exception as e:
        print(f"Exception: {e}")
        print(f"Failed to report status to {REPORT_IP}", flush=True)
        return


def startReportStatusThread():
    if REPORT_IP is None:
        return

    def reportStatusThread():
        while True:
            reportStatus()
            time.sleep(REPORT_INTERVAL_SECS)

    x = threading.Thread(target=reportStatusThread, args=())
    x.start()


if __name__ == '__main__':
    startReportStatusThread()
    app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=PORT)
