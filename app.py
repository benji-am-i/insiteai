from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import json
import urllib.request

app = Flask(__name__)
CORS(app)

# URL to the service account key
SERVICE_ACCOUNT_URL = "https://storage.googleapis.com/ai_comms/property-clients-1fba63ba6d0c.json"
SCOPES = ["https://www.googleapis.com/auth/generative-language"]

def get_service_account_credentials():
    """Fetch the service account JSON from the hosted URL and return credentials."""
    try:
        with urllib.request.urlopen(SERVICE_ACCOUNT_URL) as response:
            service_account_json = json.load(response)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_json, scopes=SCOPES
        )
        return credentials
    except Exception as e:
        print(f"Error loading service account credentials: {e}")
        raise

# Load credentials
credentials = get_service_account_credentials()

# Gemini API Endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"

@app.route('/proxy', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # Get the request payload
    data = request.get_json()

    try:
        # Refresh OAuth token
        credentials.refresh(Request())
        token = credentials.token

        # Forward the request to the Gemini API
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)

        # Log and return the Gemini API response
        print("Gemini API Response Status Code:", response.status_code)
        print("Gemini API Response Text:", response.text)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return make_response(
                jsonify({"error": f"Gemini API returned status {response.status_code}", "details": response.text}),
                response.status_code,
            )
    except Exception as e:
        print(f"Error occurred: {e}")
        return make_response(jsonify({"error": "Internal server error", "details": str(e)}), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
