from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Automatically adds CORS headers for all routes

# Gemini API endpoint and your API key
GEMINI_API_URL = "https://gemini.googleapis.com/v1beta2/models/gemini-1.5-pro:generateText"
API_KEY = "AIzaSyCHo1yOJUqDQZxC3K5l8II0XDrlCPFvYd0"  # Replace with your actual API key

@app.route('/proxy', methods=['POST', 'OPTIONS'])
def proxy():
    # Handle preflight (OPTIONS) request
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # Get the request payload
    data = request.get_json()

    # Forward the request to Gemini API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)

    # Return the response to the client
    proxy_response = make_response(response.json())
    proxy_response.headers['Access-Control-Allow-Origin'] = '*'
    return proxy_response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

