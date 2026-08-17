import random
import json
import re
import joblib
import nltk
from flask import Flask, render_template, request, jsonify
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Initialize Flask application
app = Flask(__name__)

# Download NLTK data dependencies
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Load saved ML model and vectorizer artifacts
try:
    model = joblib.load('chatbot_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    with open('responses.json', 'r') as f:
        responses_map = json.load(f)
    print("Model and datasets loaded successfully.")
except Exception as e:
    print(f"Error loading model files: {e}. Ensure train_model.py has been executed.")

def preprocess_input(text):
    """Normalize and clean user input query."""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    tokens = text.split()
    cleaned = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(cleaned) if cleaned else text

# Fallback response options when confidence threshold is not met
FALLBACK_RESPONSES = [
    "I'm sorry, I didn't quite understand your query. Could you please rephrase your question?",
    "I couldn't match your query to our information base. Try asking about admissions, fees, courses, exams, or placements!",
    "I'm still learning! Could you try asking that in a different way, or pick a topic like Fees or Facilities?"
]

@app.route('/')
def home():
    """Render the chatbot user interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages sent from the front-end JS."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'status': 'error',
                'response': 'Please enter a valid message.'
            }), 400

        # Preprocess query
        processed_query = preprocess_input(user_message)
        query_vec = vectorizer.transform([processed_query])
        
        # Calculate intent prediction probabilities
        probabilities = model.predict_proba(query_vec)[0]
        max_prob_idx = probabilities.argmax()
        max_confidence = probabilities[max_prob_idx]
        predicted_intent = model.classes_[max_prob_idx]
        
        # Set confidence threshold (35%)
        CONFIDENCE_THRESHOLD = 0.35
        
        if max_confidence < CONFIDENCE_THRESHOLD:
            bot_response = random.choice(FALLBACK_RESPONSES)
            intent_result = "fallback"
        else:
            possible_responses = responses_map.get(predicted_intent, FALLBACK_RESPONSES)
            bot_response = random.choice(possible_responses)
            intent_result = predicted_intent

        return jsonify({
            'status': 'success',
            'response': bot_response,
            'intent': intent_result,
            'confidence': round(float(max_confidence), 2)
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'response': 'An internal server error occurred. Please try again later.'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
