# Codex NLP Toolbox

[![CI](https://github.com/grunobuide/Codex-NLP-toolbox/actions/workflows/ci.yml/badge.svg)](https://github.com/grunobuide/Codex-NLP-toolbox/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-blue)](pyproject.toml)
![Coverage floor](https://img.shields.io/badge/coverage%20floor-90%25-brightgreen)

A reproducible, evaluation-driven NLP toolbox for **transparent linguistic baselines**.

Every method here is an interpretable baseline: rule-based, lexicon-based, or frequency-based, implemented from scratch with no ML dependencies. You can trace any output back to the exact heuristic that produced it. A Streamlit app wraps the library so each result can be inspected alongside an explanation of the mechanism behind it.

## Why interpretable baselines?

Before reaching for a model, you need a floor to compare against and a mechanism you can reason about. This project provides that floor: methods whose behavior is fully inspectable, so their failure modes can be documented rather than guessed. It is aimed at NLP courses, hands-on labs, and anyone who wants to understand what simple methods can and cannot do before adding complexity.

## Features

- Pure-Python NLP building blocks: sentence splitting, tokenization, n-grams, stopword filtering (real per-language lists, spaCy 3.8/MIT), keyword extraction.
- Descriptive statistics: lexical counts, word-length distribution, and readability formulas calibrated per language (Flesch, Fernández Huerta, Kandel–Moles, Amstad, Franchina–Vacca, Martins et al.).
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
| Descriptive stats | `readability_score` | language-calibrated readability formulas (see `docs/resources.md`) |
| Descriptive stats | `top_ngrams`, `word_length_distribution` | frequency counting |
| Sentiment | `sentiment_analysis` | lexicon lookup, normalized polarity |
| Information extraction | `extract_keywords` | stopword-filtered term frequency ranking |
| Language profile | `detect_language`, `language_hint_hits` | hint-word overlap with inspectable per-language evidence |
| Text structure | `split_sentences`, `tokenize_text`, `filter_tokens`, `generate_ngrams` | regex segmentation and token windows |

## Non-goals

This project deliberately does **not** aim to:

- Compete with production NLP libraries (spaCy, NLTK, Hugging Face) on accuracy or coverage.
- I
