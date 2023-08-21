from flask import Flask, request, jsonify
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()  # take environment variables from .env.
app = Flask(__name__)
fileDir = os.path.dirname(__file__)
servicesDir = os.path.join(fileDir, '../services')
print(f"servicesDir: {servicesDir}")

PORT = os.environ.get("SERVICE_FATHER_PORT", 16000)
EXPECTED_TOKEN_ID = os.environ.get("SERVICE_FATHER_TOKEN_ID", "")


def getErrorJson(service, action, completedProcess):
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


@app.route('/api', methods=['POST'])
def perform_post():
    data = request.json
    service_name = data.get('serviceName')
    action = data.get('action')
    token_id = data.get('token', None)

    # service_name = service_name.lower()
    action = action.lower()

    if not service_name or not action or not token_id:
        return jsonify({'returncode': 400, 'message': 'Service name, action, and tokenId are required.'}), 400

    if token_id != EXPECTED_TOKEN_ID:
        return jsonify({'returncode': 403, 'message': 'Incorrect tokenId. Access denied.'}), 403

    script_path = f'{servicesDir}/{service_name}/{action}.sh'
    if not os.path.isfile(script_path):
        return jsonify({'returncode': 404, 'message': f"Script '{action}.sh' not found for service '{service_name}'."}), 404

    completedProcess = subprocess.run(
        ['bash', script_path], capture_output=True)
    if completedProcess.returncode != 0:
        return getErrorJson(service_name, action, completedProcess), 500
    return getResponseJson(service_name, action, completedProcess), 200


"""
@app.route('/api/<service_name>/<action>', methods=['GET'])
def perform_action(service_name, action):
    service_name = service_name.lower()
    action = action.lower()
    script_path = f'{scriptDir}/services/{service_name}/{action}.sh'

    try:
        subprocess.run(['bash', script_path], check=True)
        return f"Action '{action}' performed for service '{service_name}'."
    except FileNotFoundError:
        return f"Script '{action}.sh' not found for service '{service_name}'."
    except subprocess.CalledProcessError:
        return f"Error while running script '{action}.sh' for service '{service_name}'."
"""

if __name__ == '__main__':

    app.run(debug=True, ssl_context='adhoc', host='0.0.0.0', port=PORT)
