# Enginews — AI-Powered News & Fake News Detection Platform

Enginews is a dynamic news platform integrated with an intelligent **SpotFake** feature that detects fake news in real time using **Machine Learning** and **Natural Language Processing (NLP)**.

The project combines a locally trained **Naive Bayes classifier** with a **Hugging Face BERT model** to improve prediction accuracy and contextual understanding of news articles. Users can explore news articles while simultaneously verifying whether the content is likely to be real or fake.

---

## Live Demo

🚀 Live Project: https://enginews.onrender.com

---

# Features

- Real-time Fake News Detection
- Dynamic News Website
- Hybrid ML + NLP Pipeline
- BERT-based Contextual Analysis
- Naive Bayes Text Classification
- REST API Integration
- Responsive UI
- Fast News Verification System

---

# Tech Stack

## Frontend
- HTML5
- CSS3
- JavaScript

## Backend
- Node.js
- Express.js
- Flask (Python API)

## Machine Learning & NLP
- Python
- Scikit-learn
- Multinomial Naive Bayes
- Hugging Face Transformers
- BERT Model
- NLP Text Preprocessing

## APIs & Tools
- REST APIs
- News API
- Git & GitHub

---

# Machine Learning Workflow

The fake news detection pipeline follows these steps:

1. News article input
2. Text preprocessing
   - Tokenization
   - Stopword removal
   - Text cleaning
3. Feature extraction using vectorization
4. Prediction using:
   - Naive Bayes model
   - BERT transformer model
5. Final authenticity result generation

---

# Model Performance

| Metric | Score |
|---|---|
| Accuracy | 94.2% |
| Precision | 93.5% |
| Recall | 95.1% |
| F1-Score | 94.3% |

---

# Project Structure

```bash
Enginews/
│
├── public/
│   ├── index.html
│   ├── fake.html
│   ├── css/
│   └── js/
│
├── model/
│   ├── app.py
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── server.js
├── package.json
└── README.md
```

---

# Installation & Setup

## Clone Repository

```bash
git clone https://github.com/rudraXWork/Enginews.git
cd Enginews
```

---

## Install Node Dependencies

```bash
npm install
```

---

## Install Python Dependencies

```bash
pip install flask scikit-learn transformers torch nltk
```

---

# Run Backend Server

## Node.js Server

```bash
node server.js
```

## Flask ML API

```bash
python app.py
```

---

# Future Improvements

- User Authentication
- News Recommendation System
- AI-based Article Summarization
- Multilingual Fake News Detection
- Dashboard Analytics
- Cloud Deployment

---

# Resume Highlights

- Built a real-time Fake News Detection system using NLP, Naive Bayes, and BERT models
- Integrated Python ML models with a Node.js web application
- Developed REST APIs for live article verification
- Achieved over 94% prediction accuracy using hybrid ML architecture

---

# GitHub Repository

GitHub: https://github.com/rudraXWork/Enginews

---

# Live Website

🌐 https://enginews.onrender.com

---

# Author

## Rudra Narayan Jena
B.Tech CSE (Data Science)  
Machine Learning & Full Stack Development Enthusiast
