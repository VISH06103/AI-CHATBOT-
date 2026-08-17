import pandas as pd
import numpy as np
import json
import re
import joblib
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Download NLTK data dependencies
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """Clean, tokenize, remove special characters, and lemmatize text."""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    tokens = text.split()
    cleaned_tokens = [
        lemmatizer.lemmatize(word) for word in tokens if word not in stop_words
    ]
    return " ".join(cleaned_tokens) if cleaned_tokens else text

def train_chatbot():
    print("Loading dataset...")
    df = pd.read_csv('dataset.csv')
    
    # Preprocess text column
    df['cleaned_question'] = df['question'].apply(preprocess_text)
    
    X = df['cleaned_question']
    y = df['intent']
    
    # Build intent to responses mapping dictionary
    intent_responses = {}
    for intent, group in df.groupby('intent'):
        intent_responses[intent] = group['response'].unique().tolist()
        
    # Vectorize using TF-IDF with unigrams and bigrams
    print("Extracting TF-IDF features...")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_vec = vectorizer.fit_transform(X)
    
    # Train Naive Bayes Classifier
    print("Training Machine Learning Model (Multinomial Naive Bayes)...")
    model = MultinomialNB(alpha=0.1)
    model.fit(X_vec, y)
    
    # Model evaluation
    y_pred = model.predict(X_vec)
    accuracy = accuracy_score(y, y_pred)
    print(f"\nModel Training Completed!")
    print(f"Training Accuracy: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y, y_pred))
    
    # Export trained artifacts
    print("Saving model artifacts...")
    joblib.dump(model, 'chatbot_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    
    with open('responses.json', 'w') as f:
        json.dump(intent_responses, f, indent=4)
        
    print("All artifacts exported successfully!")

if __name__ == "__main__":
    train_chatbot()
