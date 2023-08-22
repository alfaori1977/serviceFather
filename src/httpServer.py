from flask import Flask, request, jsonify
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()  # take environment variables from .env.
app = Flask(__name__)
scriptDir = os.path.dirname(__file__)

PORT = os.environ.get("SERVICE_FATHER_PORT",16000)
EXPECTED_TOKEN_ID = os.environ.get("SERVICE_FATHER_TOKE_ID","")

@app.route('/api', methods=['POST'])
def perform_post():
    data = request.json
    service_name = data.get('serviceName')
    action = data.get('action')
    token_id = data.get('token', None)

    #service_name = service_name.lower()
    action = action.lower()

    if not service_name or not action or not token_id:
        return jsonify({'error': 'Service name, action, and tokenId are required.'}), 400
    
    if token_id != EXPECTED_TOKEN_ID:
        return jsonify({'error': 'Incorrect tokenId. Access denied.'}), 403
    
    script_path = f'{scriptDir}/services/{service_name}/{action}.sh'

    try:
        subprocess.run(['bash', script_path], check=True)
        return jsonify({'message': f"Action '{action}' performed for service '{service_name}'."})
    except FileNotFoundError:
        return jsonify({'error': f"Script '{action}.sh' not found for service '{service_name}'."}), 404
    except subprocess.CalledProcessError:
        return jsonify({'error': f"Error while running script '{action}.sh' for service '{service_name}'."}), 500

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
