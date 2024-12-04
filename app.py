from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Gemini API endpoint and your API key
GEMINI_API_URL = "https://gemini.googleapis.com/v1beta2/models/gemini-1.5-pro:generateText"
API_KEY = "AIzaSyCHo1yOJUqDQZxC3K5l8II0XDrlCPFvYd0"

@app.route('/proxy', methods=['POST'])
def proxy():
    # Get the request payload
    data = request.get_json()

    # Forward the request to Gemini API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)

    # Return the response to the client
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
