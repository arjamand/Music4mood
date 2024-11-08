from flask import Flask, render_template, request, jsonify
import numpy as np
import os
from tensorflow.keras.models import load_model
import pickle
from model.user_function import predict_sentiment  # Import your function from user_function.py

app = Flask(__name__)

# Load model and tokenizer
MODEL_PATH = "model/sentiment_analysis.keras"
TOKENIZER_PATH = "model/tokenizer.pickle"
MAX_LENGTH = 63  # Length used during training

model = load_model(MODEL_PATH)    
with open(TOKENIZER_PATH, 'rb') as handle:
    tokenizer = pickle.load(handle)

# Define mood categories
MOOD_CATEGORIES = {
    "sadness": "sadness-sad",
    "joy": "joy-happy",
    "love": "love-relaxed",
    "anger": "anger-energetic",
    "fear": "fear-thoughtful",
    "surprise": "surprise-happy"
}

# Route for main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle mood input and return a mood category
@app.route('/get-mood', methods=['POST'])
def get_mood():
    data = request.get_json()
    mood_text = data.get("mood", "")

    # Get the predicted sentiment category using the model
    mood_label = predict_sentiment(mood_text, tokenizer, MAX_LENGTH)
    mood_category = MOOD_CATEGORIES.get(mood_label, "relaxed")  # Default to "relaxed" if unknown
    
    return jsonify({"moodCategory": mood_category})

if __name__ == "__main__":
    app.run(debug=True)
