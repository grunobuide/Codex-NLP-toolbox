# Codex NLP Toolbox

A reproducible, evaluation-driven NLP toolbox for **transparent linguistic baselines**.

Every method here is an interpretable baseline: rule-based, lexicon-based, or frequency-based, implemented from scratch with no ML dependencies. You can trace any output back to the exact heuristic that produced it. A Streamlit app wraps the library so each result can be inspected alongside an explanation of the mechanism behind it.

## Why interpretable baselines?

Before reaching for a model, you need a floor to compare against and a mechanism you can reason about. This project provides that floor: methods whose behavior is fully inspectable, so their failure modes can be documented rather than guessed. It is aimed at NLP courses, hands-on labs, and anyone who wants to understand what simple methods can and cannot do before adding complexity.

## Features

- Pure-Python NLP building blocks: sentence splitting, tokenization, n-grams, stopword filtering, keyword extraction.
- Descriptive statistics: lexical counts, word-length distribution, Flesch Reading Ease.
- Lexicon-based sentiment analysis with normalized polarity score.
- Heuristic language detection (English, Spanish, French, German, Italian, Portuguese) with per-language evidence you can inspect.
- Streamlit UI where every result is paired with a what/how/why explanation of the method.

## Installation

Requires Python 3.10–3.13. With [uv](https://docs.astral.sh/uv/) (recommended):

```bash
git clone https://github.com/grunobuide/Codex-NLP-toolbox.git
cd Codex-NLP-toolbox
uv sync                # reproducible install from uv.lock
uv run streamlit run app.py
```

With pip:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
streamlit run app.py
```

For development (tests included):

```bash
uv sync --group dev
uv run pytest
```

## Method catalog

| Category | Function | Mechanism |
|---|---|---|
| Descriptive stats | `analyze_text` | text-level counts and lexical metrics |
| Descriptive stats | `readability_score` | Flesch Reading Ease via sentence/word/syllable heuristics |
| Descriptive stats | `top_ngrams`, `word_length_distribution` | frequency counting |
| Sentiment | `sentiment_analysis` | lexicon lookup, normalized polarity |
| Information extraction | `extract_keywords` | stopword-filtered term frequency ranking |
| Language profile | `detect_language`, `language_hint_hits` | hint-word overlap with inspectable per-language evidence |
| Text structure | `split_sentences`, `tokenize_text`, `filter_tokens`, `generate_ngrams` | regex segmentation and token windows |

## Non-goals

This project deliberately does **not** aim to:

- Compete with production NLP libraries (spaCy, NLTK, Hugging Face) on accuracy or coverage.
- Include machine-learned models, embeddings, or LLM calls — every method stays hand-inspectable.
- Serve as production infrastructure. There is no API server, orchestration, or deployment tooling beyond the demo app.
- Support every language. Language-aware features cover six European languages via explicit lexicons.

If a task needs state-of-the-art accuracy, use these methods as the baseline to beat, not the solution.

