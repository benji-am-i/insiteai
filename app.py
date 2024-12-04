from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import json
import urllib.request

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
SERVICE_ACCOUNT_URL = "https://storage.googleapis.com/ai_comms/property-clients-1fba63ba6d0c.json"  # Your service account key
SCOPES = ["https://www.googleapis.com/auth/generative-language"]
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"

def get_service_account_credentials():
    """Fetch and return service account credentials from the hosted URL."""
    try:
        with urllib.request.urlopen(SERVICE_ACCOUNT_URL) as response:
            service_account_json = json.load(response)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_json, scopes=SCOPES
        )
        print("Service account credentials loaded successfully.")
        return credentials
    except Exception as e:
        print(f"Error loading service account credentials: {e}")
        raise

# Load service account credentials
credentials = get_service_account_credentials()

@app.route('/proxy', methods=['POST', 'OPTIONS'])
def proxy():
    """Proxy route to forward requests to the Gemini API."""
    if request.method == 'OPTIONS':
        # Handle preflight CORS requests
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
        print(f"Generated OAuth 2.0 Token: {token}")

        # Forward the request to the Gemini API
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        print(f"Forwarding request to Gemini API: {GEMINI_API_URL}")
        print(f"Request Payload: {json.dumps(data)}")

        response = requests.post(GEMINI_API_URL, headers=headers, json=data)

        # Log and return the Gemini API response
        print(f"Gemini API Response Status Code: {response.status_code}")
        print(f"Gemini API Response Body: {response.text}")

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return make_response(
                jsonify({"error": f"Gemini API returned status {response.status_code}", "details": response.text}),
                response.status_code,
            )
    except Exception as e:
        # Log and handle errors
        print(f"Error occurred: {e}")
        return make_response(jsonify({"error": "Internal server error", "details": str(e)}), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
