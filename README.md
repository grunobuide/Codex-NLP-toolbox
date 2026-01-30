# Codex NLP Toolbox

A lightweight, classroom-friendly NLP toolbox for Python users. The goal is to help students and learners **upload raw text**, run **multiple NLP techniques**, and immediately see how the techniques behave across **different languages**.

## ✨ Features
- Upload text files or paste raw text.
- Language-aware processing with simple language detection heuristics.
- NLP building blocks: sentence splitting, tokenization, n-grams, keyword extraction, frequency tables.
- Designed for **learning and experimentation** rather than heavy production pipelines.

## 🚀 Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the provided local URL in your browser.

## 📁 Project Structure
```
.
├── app.py               # Streamlit UI
├── nlp_toolbox/
│   ├── __init__.py
│   ├── languages.py     # Language configuration + stopwords
│   └── tools.py         # Core NLP utilities
└── requirements.txt
```

## 🧠 Designed for NLP Courses
This repo focuses on **transparent, minimal implementations** to make the inner workings of NLP tools easy to explore. It is ideal for:
- Intro NLP lectures
- Hands-on labs
- Student experimentation

## 🔧 Extending the Toolbox
Add additional tools (lemmatizers, POS taggers, NER, transformers) by plugging in libraries like spaCy, NLTK, or HuggingFace. Keep new tools in `nlp_toolbox/tools.py` or create new modules and expose them in `app.py`.

## 📝 License
MIT
