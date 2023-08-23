import os
from dotenv import load_dotenv
import pprint
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import threading
import time
import json

from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
CORS(app)  # allow CORS for all routes


serverInfo = [
    {
        'name': 'SF_0',
        'hostname': 'localhost',
        'port': 26000},
    {
        'name': 'SF_1',
        'hostname': 'localhost',
        'port': 26001
    },
    {
        'name': 'SF_2',
        'hostname': 'localhost',
        'port': 26002
    },

    {
        'name': 'SF_3',
        'hostname': 'server3',
        'port': 26002
    },
]


"""
globalStatus = {'result': []}
def updateStatus():
    # Dictionary to store the status of each node
    node_status = []
    for server in serverInfo:
        url = f'https://{server["hostname"]}:{server["port"]}/api/services'
        # try to get the status of the node else set it to offline
        try:
            response = requests.get(url, verify=False,  timeout=1)
            if response.status_code == 200:
                services = response.json()
                node_status.append({
                    'name': server["name"],
                    'services': services,
                    'hostname': server['hostname'],
                    'port': server['port']
                })
        except Exception as e:
            node_status.append({
                'name': server["name"],
                'status': str(e),
                'services': [],
                'hostname': server['hostname'],
                'port': server['port']
            })
    globalStatus['result'] = node_status
    pprint.pprint(globalStatus)

"""

globalStatus = {}


@app.route('/status', methods=['POST'])
def update_status():
    # Get the node ID and status from the request JSON data
    data = request.get_json()
    rAddr = request.remote_addr
    print("rAddr: ", request)
    print("data: ", data)
    for srv in data:
        srv['rAddr'] = rAddr
        srv['lastUpdate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        key = f"{srv['service']}@{rAddr}:{srv['port']}"
        globalStatus[key] = srv

    print("globalStatusDict: ", json.dumps(globalStatus, indent=4))
    return jsonify({'message': 'Global Status fupdated'}), 200


@app.route('/status', methods=['GET'])
def status():
    # Return the current status of all nodes
    pprint.pprint(globalStatus)
    responseList = []
    for key in globalStatus:
        globalStatus[key]['id'] = key
        responseList.append(globalStatus[key])

    return jsonify({'result': responseList}), 200


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


def updateStatusThread():
    while True:
        updateStatus()
        time.sleep(5)


def startStatusThread():
    x = threading.Thread(target=updateStatusThread, args=())
    x.start()


SRV_PORT = os.environ.get("SERVICE_FATHER_MGR_PORT", 15001)

if __name__ == '__main__':
    # run updateStatus() every 5 seconds in a Thread usin python Threads
    # startStatusThread()
    # pprint.pprint(node_status)
    app.run(host='0.0.0.0', port=SRV_PORT)
