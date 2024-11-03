from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Placeholder function for mood classification
def get_mood_category(mood_text):
    # Replace this with actual model call
    categories = ["happy", "sad", "relaxed", "energetic", "thoughtful"]
    return random.choice(categories)

# Route to handle mood input and return category
@app.route('/get-mood', methods=['POST'])
def get_mood():
    data = request.get_json()
    mood_text = data.get("mood", "")
    mood_category = get_mood_category(mood_text)
    return jsonify({"moodCategory": mood_category})

if __name__ == "__main__":
    app.run(debug=True)
