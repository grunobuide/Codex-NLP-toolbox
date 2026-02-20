# Codex NLP Toolbox

A lightweight, classroom-friendly NLP toolbox for Python users. The goal is to help students and learners **upload raw text**, run **multiple NLP techniques**, and immediately see how the techniques behave across **different languages**.

The app is intentionally built for **explainable NLP workflows**: each tool includes context for:
- what the tool does,
- how it works internally,
- why it is useful,
- what to explore next.

## ✨ Features
- Upload text files or paste raw text.
- Language-aware processing with simple language detection heuristics.
- NLP building blocks: sentence splitting, tokenization, n-grams, keyword extraction, frequency tables.
- Thematic organization of tools (descriptive stats, sentiment, information extraction, language profile, text structure).
- Built-in method catalog for step-by-step technique explanations.
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

## 🧭 NLP Tool Taxonomy

### Descriptive statistics
- `analyze_text`: text-level counts and lexical metrics.
- `readability_score`: Flesch Reading Ease using sentence/word/syllable heuristics.
- `top_ngrams`: most frequent phrase patterns.
- `word_length_distribution`: token-length profile.

### Sentiment analysis
- `sentiment_analysis`: lexicon-based positive/negative count and normalized polarity score.

### Information extraction
- `extract_keywords`: stopword-filtered term frequency ranking.

### Language profile
- `detect_language`: hint-word overlap across supported languages.
- `language_hint_hits`: per-language evidence for explainable detection.

### Text structure
- `split_sentences`: regex sentence segmentation.
- `tokenize_text`: regex word tokenization.
- `filter_tokens`: stopword/min-length filtering.
- `generate_ngrams`: contiguous token windows.

## 🔍 Explainability-First Workflow
Each result in the app can be read in two layers:
1. **Processing output** (metrics, lists, distributions).
2. **Method explanation** (what/how/why/explore-next) so users can inspect assumptions and limitations.

This design helps learners understand both the output and the mechanism that produced it.

## 🧠 Designed for NLP Courses
This repo focuses on **transparent, minimal implementations** to make the inner workings of NLP tools easy to explore. It is ideal for:
- Intro NLP lectures
- Hands-on labs
- Student experimentation

## 🔧 Extending the Toolbox
Add additional tools (lemmatizers, POS taggers, NER, transformers) by plugging in libraries like spaCy, NLTK, or HuggingFace. Keep new tools in `nlp_toolbox/tools.py` or create new modules and expose them in `app.py`.

## 📝 License
MIT
