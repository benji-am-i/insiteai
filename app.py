from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Gemini API endpoint and your API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
API_KEY = "AIzaSyCHo1yOJUqDQZxC3K5l8II0XDrlCPFvYd0"  # Replace with your actual API key

@app.route('/proxy', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # Get the request payload from the client
    data = request.get_json()

    try:
        # Forward the request to the Gemini API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)

        # Log the Gemini API response
        print("Gemini API Response Status Code:", response.status_code)
        print("Gemini API Response Text:", response.text)

        # Return the Gemini API response to the client
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            # Handle non-200 responses
            return make_response(
                jsonify({"error": f"Gemini API returned status {response.status_code}", "details": response.text}),
                response.status_code,
            )
    except Exception as e:
        # Log the exception
        print("Error occurred:", e)
        return make_response(jsonify({"error": "Internal server error", "details": str(e)}), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)




