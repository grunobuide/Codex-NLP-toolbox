# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Added

- Character n-gram language detection (Cavnar–Trenkle 1994) with shipped
  Wikipedia-trained trigram profiles: 98.9% language-ID accuracy vs 75.6%
  for hint-words; 61% vs 29% on 2-word inputs. New benchmark row and probe.
- Collocations via PMI and log-likelihood ratio (Dunning 1993); CLI
  `codex-nlp collocations`.
- Porter stemmer (English) with documented over-stemming cases; CLI
  `codex-nlp stem`.
- CLI `codex-nlp language` for language identification: `--method char-ngram`
  (default) or `--method hints`, and `--compare` to run both detectors side by
  side and report agreement.
- Provenance manifest and reproducible build script
  (`scripts/build_ngram_profiles.py`) for the char n-gram profiles, plus a
  `NOTICE` separating code (MIT) from Wikipedia-derived profiles (CC BY-SA 4.0)
  and evaluation datasets (upstream licenses).

Planned (see [ROADMAP.md](ROADMAP.md) and [CONTENT_ROADMAP.md](CONTENT_ROADMAP.md)):
method handbook with hand-computed examples, case-study notebooks, instructor
guide, bilingual documentation layer, lesson mode.

## [1.0.0] — 2026-07-14

First stable release: *a reproducible, evaluation-driven NLP toolbox for
transparent linguistic baselines.*

### Added

- **Library** (`nlp_toolbox`): sentence splitting, tokenization, n-grams,
  stopword filtering, frequency and TF-IDF keyword extraction, KWIC
  concordance, Zipf rank–frequency table, vocabulary growth curve,
  lexicon sentiment analysis, hint-word language detection with explicit
  evidence (`detect_language_details`: scores, ties, English fallback).
- **Linguistic resources** with documented provenance (`docs/resources.md`):
  stopword lists for six languages (adapted from spaCy 3.8, MIT),
  hand-curated sentiment lexicons for six languages (~75–105 words per
  polarity), readability formulas calibrated per language with academic
  citations (Flesch, Fernández Huerta, Kandel–Moles, Amstad,
  Franchina–Vacca, Martins et al.).
- **CLI** `codex-nlp` with `analyze`, `keywords`, `kwic`, `zipf`
  subcommands and stable `--json` output.
- **Streamlit app** with three modes — Analyze (method cards, JSON export),
  Compare two texts, Benchmarks — deployed at
  https://codex-nlp-toolbox.streamlit.app with licensed sample texts in six
  languages.
- **Evaluation harness** (`evals/`): frozen licensed datasets
  (`evals/DATASETS.md`), hand-implemented metrics, JSON results with git
  SHA and dataset SHA-256, auto-generated `docs/benchmarks.md`. Measured
  against langdetect (language ID), VADER (sentiment) and pysbd
  (segmentation).
- **Error analysis** (`docs/error-analysis.md`): failure taxonomy with
  measured numbers, inherent-vs-fixable classification, robustness probes.
- **Quality gates**: ruff, mypy strict, pytest with 90% coverage floor,
  Hypothesis property tests, adversarial regression fixtures, pre-commit,
  CI matrix on Python 3.10–3.13 with wheel install smoke test.

### Fixed

- `vocabulary_growth(step=0)` raised `ZeroDivisionError`; now a documented
  `ValueError` (found by property-based testing).
- Compare-mode sample selector froze its initial value
  (Streamlit widget-state key collision).
