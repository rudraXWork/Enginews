from flask import Flask, render_template, request, jsonify
import pickle
import os
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# Access environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# Set paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

# Load the model and vectorizer
with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

# Initialize Flask app
app = Flask(__name__, template_folder="../templates", static_folder="../static")
##
@app.route('/news')
def get_news():
    query = request.args.get('q', 'fake news')  # Default topic if none is provided
    news_url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    
    try:
        response = requests.get(news_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch news', 'details': str(e)}), 500

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# SpotFake page
@app.route("/spotfake")
def spotfake():
    return render_template("fake.html")

# Predict route
@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    news = data.get("news", "")

    if not news.strip():
        return jsonify({"verdict": "Empty input"})

    # Transform and predict
    x_input = vectorizer.transform([news])
    prediction = model.predict(x_input)[0]  # Assumes 0=FAKE, 1=REAL

    verdict = "REAL" if prediction == 1 else "FAKE"
    return jsonify({"verdict": verdict})

# Run server
if __name__ == "__main__":
    app.run(debug=True)
