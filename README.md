# Codex NLP Toolbox

[![CI](https://github.com/grunobuide/Codex-NLP-toolbox/actions/workflows/ci.yml/badge.svg)](https://github.com/grunobuide/Codex-NLP-toolbox/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-blue)](pyproject.toml)
![Coverage floor](https://img.shields.io/badge/coverage%20floor-90%25-brightgreen)

A reproducible, evaluation-driven NLP toolbox for **transparent linguistic baselines**.

**[Live demo](https://codex-nlp-toolbox.streamlit.app)** — analyze text in six languages, compare two texts side by side, and inspect the benchmark results, no setup required.

[![Demo: analyze, compare and benchmark modes](docs/codex-nlp-toolbox-demo.gif)](https://codex-nlp-toolbox.streamlit.app)

Every method here is an interpretable baseline: rule-based, lexicon-based, or frequency-based, implemented from scratch with no ML dependencies. You can trace any output back to the exact heuristic that produced it. A Streamlit app wraps the library so each result can be inspected alongside an explanation of the mechanism behind it.

## Why interpretable baselines?

Before reaching for a model, you need a floor to compare against and a mechanism you can reason about. This project provides that floor: methods whose behavior is fully inspectable, so their failure modes can be documented rather than guessed. It is aimed at NLP courses, hands-on labs, and anyone who wants to understand what simple methods can and cannot do before adding complexity.

## Features

- Pure-Python NLP building blocks: sentence splitting, tokenization, n-grams, stopword filtering (real per-language lists, spaCy 3.8/MIT), keyword extraction.
- Descriptive statistics: lexical counts, word-length distribution, and readability formulas calibrated per language (Flesch, Fernández Huerta, Kandel–Moles, Amstad, Franchina–Vacca, Martins et al.).
- Lexicon-based sentiment analysis in all six languages (hand-curated v1 lexicons, documented methodology).
- Two language detectors for six languages (English, Spanish, French, German, Italian, Portuguese) with inspectable per-language evidence: character n-grams (Cavnar–Trenkle, the recommended default) and hint words (a transparent baseline that shows exactly *which words* decided).
- Streamlit UI where every result is paired with a what/how/why explanation of the method, with an English / Brazilian-Portuguese toggle for all didactic text (code, APIs and JSON output stay English).

Language coverage is layered and stated precisely: interface and linguistic resources cover all six languages; sentiment and segmentation *evaluation* is English-only (gold datasets); the Porter stemmer is English-only. Details: [CONTENT_ROADMAP.md](CONTENT_ROADMAP.md).

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

## Command line

The same baselines, scriptable. After installing:

```bash
codex-nlp analyze data/samples/frankenstein_en.txt --json   # full profile
codex-nlp keywords text.txt --method tfidf --top-k 15       # freq or tfidf
codex-nlp kwic text.txt love --window 5                     # concordance
codex-nlp zipf text.txt --top-k 50                          # rank-frequency
codex-nlp collocations text.txt --min-count 3 --top-k 20    # bigrams (PMI + LLR)
codex-nlp stem running runs ran --json                      # Porter stems (English)
codex-nlp language text.txt --method char-ngram             # language ID (or: hints)
codex-nlp language text.txt --compare --json                # both detectors + agreement
```

Language is auto-detected (`--lang` to override); `--json` gives stable, machine-readable output for pipelines. The CLI computes collocations over the original token sequence, so bigram adjacency matches the source text.

## Method catalog

| Category | Function | Mechanism |
|---|---|---|
| Descriptive stats | `analyze_text` | text-level counts and lexical metrics |
| Descriptive stats | `readability_score` | language-calibrated readability formulas (see `docs/resources.md`) |
| Descriptive stats | `top_ngrams`, `word_length_distribution` | frequency counting |
| Sentiment | `sentiment_analysis` | lexicon lookup, normalized polarity |
| Information extraction | `extract_keywords` | stopword-filtered term frequency ranking |
| Information extraction | `tfidf_keywords` | tf x log10(N/df), sentences as documents |
| Information extraction | `collocations` | adjacent bigrams ranked by log-likelihood ratio (Dunning 1993) with PMI |
| Descriptive stats | `zipf_table`, `vocabulary_growth` | rank-frequency (Zipf) and type-token growth |
| Text structure | `kwic` | keyword-in-context concordance |
| Text structure | `porter_stem` | Porter (1980) suffix-stripping stemmer for English |
| Language profile | `detect_language_details`, `language_hint_hits`, `language_hint_evidence` | hint-word overlap; ties, English fallback and the exact matching words reported explicitly |
| Language profile | `detect_language_ngram_details` | character trigram profiles, Cavnar–Trenkle out-of-place distance (recommended default) |
| Text structure | `split_sentences`, `tokenize_text`, `filter_tokens`, `generate_ngrams` | regex segmentation and token windows |

## Benchmarks

Measured, not asserted — full tables, confusion matrices and dataset provenance in [docs/benchmarks.md](docs/benchmarks.md), reproducible with `uv sync --group evals && uv run python -m evals.run --task <task>`:

| Task (dataset) | Toolbox baseline | External system |
|---|---|---|
| Language ID (180 Gutenberg sentences, 6 langs) | hint-words: 75.6% / char-ngrams: **98.9%** | langdetect: 99.4% acc |
| Binary sentiment EN (120 UCI review sentences) | v1 lexicon: 76.7% acc | VADER: 80.0% acc |
| Sentence segmentation EN (60 UD-EWT gold) | regex: F1 0.919 | pysbd: F1 0.975 |

On this small frozen dataset the char n-gram baseline made **one more error than langdetect** (≈178 vs ≈179 correct out of 180) — the accuracies are close, not evidence of statistical equivalence. The set has only 30 sentences per language drawn from a single literary work per language, so treat the gap as indicative, not conclusive (provenance and known biases: [docs/benchmarks.md](docs/benchmarks.md)). Planned benchmark hardening: confidence intervals, absolute error counts, other domains, real short texts, code-switching, and orthographic noise.

The transparent baselines are *expected* to lose to specialized systems — the value is knowing by how much, and why: see the [error analysis](docs/error-analysis.md), where every failure mode is measured, classified as inherent or fixable, and pinned by a regression test.

## Teaching with this project

The toolbox doubles as course material for **"Fundamentos transparentes de
PLN: do texto à avaliação"** (7 lessons, PT-BR, for linguistics students
with no programming prerequisite — syllabus in
[docs/course/syllabus.md](docs/course/syllabus.md)):

- **Handbook**: hand-computable method pages in [docs/handbook/](docs/handbook/) — every number reproducible with pencil and paper.
- **Lesson packages**: versioned recording presets and exercises with commented answer keys in [docs/course/](docs/course/); every quoted result is pinned by `tests/test_lesson_presets.py`, so scripts can never drift silently from the app.
- **Editorial contract and plan**: [docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md](docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md).

## Project status

**Stable and usable; content production paused.** The engineering track
([ROADMAP.md](ROADMAP.md), phases 0–6) is complete: library, CLI, app,
eval harness, error analysis, quality gates and release automation are
done and tested (112 tests, 90% coverage floor, CI on Python 3.10–3.13).
The content track ([CONTENT_ROADMAP.md](CONTENT_ROADMAP.md)) is paused
mid-pilot with no half-broken state: the lesson-4 pilot package
(handbook page, preset, exercises) is finished and test-pinned; what
remains (video, lesson page, notebooks) is listed there with its open
decisions. To pick the project up, start with
[CONTRIBUTING.md](CONTRIBUTING.md).

## Non-goals

This project deliberately does **not** aim to:

- Compete with production NLP libraries (spaCy, NLTK, Hugging Face) on accuracy or coverage.
- Introduce machine-learned or statistical models: every method is rule-, lexicon-, or frequency-based so its behavior stays fully inspectable.
- Support languages beyond the six covered (English, Spanish, French, German, Italian, Portuguese).
- Optimize for large-scale or low-latency production workloads; the priority is clarity, not throughput.
- Replace a linguistics or NLP course — it complements one by making baseline mechanisms transparent.
