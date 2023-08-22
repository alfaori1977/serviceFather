import pprint
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import threading
import time

from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
CORS(app)  # allow CORS for all routes

# Dictionary to store the status of each node
node_status = {}

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


def updateStatus():
    for server in serverInfo:
        url = f'https://{server["hostname"]}:{server["port"]}/api/services'
        # try to get the status of the node else set it to offline
        try:
            response = requests.get(url, verify=False,  timeout=1)
            if response.status_code == 200:
                services = response.json()
                node_status[server["name"]] = {
                    'services': services,
                    'hostname': server['hostname'],
                    'port': server['port']
                }
        except Exception as e:
            node_status[server["name"]] = {
                'status': str(e),
                'services': [],
                'hostname': server['hostname'],
                'port': server['port']
            }


@app.route('/status', methods=['GET'])
def status():
    # Return the current status of all nodes
    return jsonify(node_status)


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
    startStatusThread()
    pprint.pprint(node_status)
    app.run(host='0.0.0.0', port=SRV_PORT)
