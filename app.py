from flask import Flask, render_template, request, jsonify
import numpy as np
import os
import pandas as pd
import random
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

def get_song_recommendations(mood_category):
    """
    Get 5 random song recommendations from the appropriate data.csv file
    """
    try:
        # Construct the path to the data.csv file for the given mood category
        csv_path = f"static/audio/{mood_category}/data.csv"

        # print(csv_path)
        
        # Read the CSV file
        df = pd.read_csv(csv_path)
        
        # Randomly select 5 songs
        selected_songs = df.sample(n=min(5, len(df))).to_dict('records')
        
        return selected_songs
    except Exception as e:
        print(f"Error reading song recommendations: {e}")
        return []  # Return empty list if there's an error

# Route for main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle mood input and return a mood category
@app.route('/get-mood', methods=['POST'])
def get_mood():
    try:
        data = request.get_json()
        mood_text = data.get("mood", "")
        
        # Get the predicted sentiment category using the model
        mood_label = predict_sentiment(mood_text, tokenizer, MAX_LENGTH)
        mood_category = MOOD_CATEGORIES.get(mood_label, "relaxed")  # Default to "relaxed" if unknown
        
        # Get song recommendations for the mood category
        songs = get_song_recommendations(mood_category)

        return jsonify({
            "moodCategory": mood_category,
            "songs": songs
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)