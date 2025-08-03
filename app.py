import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cohere
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    recipient = data.get('recipient')
    purpose = data.get('purpose')
    tone = data.get('tone')
    email_type = data.get('type')

    # Input validation
    if not all([recipient, purpose, tone, email_type]):
        return jsonify({"error": "All fields are required."}), 400

    # Create a prompt for the email
    prompt = f"Write a {tone} {email_type} email to {recipient} about: {purpose}."

    try:
        # Use Cohere's chat endpoint
        response = co.chat(
            model="command-r",  # This model works with chat only
            message=prompt,
            temperature=0.7,
            max_tokens=300
        )
        return jsonify({"email": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
