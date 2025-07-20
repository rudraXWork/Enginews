import os
import pandas as pd
import re
import nltk
import pickle
import requests
import time
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


API_TOKEN = os.getenv("API_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")
MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text


def train_and_save_model():
    print("Training local model...")
    true = pd.read_csv("C:\html\project_1\True.csv")
    fake = pd.read_csv("C:\html\project_1\Fake.csv")

    true['label'] = 1
    fake['label'] = 0
    news = pd.concat([true, fake], axis=0)
    news = news.drop(['title', 'subject', 'date'], axis=1)
    news = news.sample(frac=1).reset_index(drop=True)
    news['text'] = news['text'].apply(clean_text)

    X = news['text']
    y = news['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    print("Model and vectorizer saved.")


if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    train_and_save_model()

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)



def check_local_model(text):
    try:
        vectorized_text = vectorizer.transform([clean_text(text)])
        prediction = model.predict(vectorized_text)[0]
        return "REAL" if prediction == 1 else "FAKE"
    except Exception as e:
        print("Local model error:", e)
        return "ERROR"

def check_hf_model(text):
    try:
        url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        payload = {"inputs": text}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 503:
            print("Model is loading, retrying...")
            time.sleep(5)
            return check_hf_model(text)

        output = response.json()
        if isinstance(output, list) and len(output) > 0:
            label = output[0][0]["label"]
            return "REAL" if "LABEL_1" in label.upper() or "REAL" in label.upper() else "FAKE"
        elif isinstance(output, dict) and "error" in output:
            print("Hugging Face Error:", output["error"])
            return "ERROR"
        else:
            print("Unexpected HF response:", output)
            return "UNKNOWN"

    except Exception as e:
        print("Exception calling Hugging Face:", e)
        return "ERROR"

def combined_prediction(text):
    local_result = check_local_model(text)
    hf_result = check_hf_model(text)

    print(f"Local Model: {local_result}")
    print(f"Hugging Face: {hf_result}")

    if "REAL" in (local_result, hf_result):
        return "REAL"
    elif "FAKE" in (local_result, hf_result):
        return "FAKE"
    else:
        return "ERROR"

# ========== TEST ==========
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
        result = combined_prediction(input_text)
        print(result)
    else:
        print("ERROR: No input provided")