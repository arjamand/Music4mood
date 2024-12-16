import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle

# Load your trained model
# model = load_model('model/sentiment_analysis.keras')

# Load the tokenizer from file
# with open('model/tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)

# Define the sentiment labels
emotion_labels = {0: 'sadness', 1: 'joy', 2: 'love', 3: 'anger', 4: 'fear', 5: 'surprise'}

def predict_sentiment(user_input, max_length=60):
    
    with open('model/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    model = load_model('model/sentiment_analysis.keras')
    # Preprocess input (tokenizing and padding

    input_seq = tokenizer.texts_to_sequences([user_input])
    input_pad = pad_sequences(input_seq, maxlen=max_length, padding='post')

    # Make a prediction
    prediction = model.predict(input_pad)
    
    # Get the sentiment with the highest probability
    predicted_label = np.argmax(prediction, axis=1)[0]
    
    # Map the predicted label to the sentiment
    predicted_sentiment = emotion_labels[predicted_label]
    
    return predicted_sentiment

# Example usage
# user_input = "i am very lonely and empty"
# predicted_sentiment = predict_sentiment(user_input, tokenizer, max_length=63)
# print(f"Predicted sentiment: {predicted_sentiment}")
