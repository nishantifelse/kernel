from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini API
API_KEY = "AIzaSyCJtM3QUw-5OTpFuH9j4VwHmXls9NUeiPQ"
genai.configure(api_key=API_KEY)

# Set up the model
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get user query from request
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Generate response using Gemini
        response = model.generate_content(user_query)
        
        # Return the response
        return jsonify({
            "response": response.text
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Check if API key is set
    if not API_KEY:
        print("Warning: GEMINI_API_KEY not set in environment variables.")
        print("Create a .env file with GEMINI_API_KEY=your_api_key_here")
    
    # Run the Flask app
    app.run(debug=True, port=5000)