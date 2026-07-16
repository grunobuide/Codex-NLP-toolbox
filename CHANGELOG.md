# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning: [SemVer](https://semver.org/).

## [1.1.0] — 2026-07-16

Language identification matured into the flagship feature (char n-gram
detector as operational default, full evidence explainability, provenance
and licensing hardened), plus the bilingual didactic layer and the first
course lesson package.

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
- Bilingual didactic layer (`app_i18n.py`): EN / PT-BR toggle for the app's
  on-screen didactic text — method cards, section headers, captions, sidebar
  labels and tab names. Code, APIs, tool names and JSON output stay English.
  Key-parity tests (`tests/test_i18n.py`) guard against missing translations.
- `language_hint_evidence()`: per language, the exact hint tokens that
  matched and how often — the app's hint table now shows *which words
  decided*, not just counts (full explainability for the course's lesson 4).
- Content QA: course renamed to "Fundamentos transparentes de PLN: do texto
  à avaliação"; syllabus aligned with the app (sample excerpts vs full-novel
  notebooks, English-only Porter examples, no hard-coded numbers in scripts);
  editorial contract and pilot plan in
  `docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md`; language-coverage
  matrix in `CONTENT_ROADMAP.md`.
- Lesson-4 pilot package (course vertical slice, app-side): first handbook
  page (`docs/handbook/deteccao-de-idioma.md`, hand-computable examples for
  both detectors), versioned recording preset with expected results pinned
  by `tests/test_lesson_presets.py`, and exercises with commented answer key
  (`docs/course/aula-04/`). Every number quoted in the materials is
  reproduced by the test suite, including two honest findings: the two
  transparent detectors disagree on ambiguous inputs ("que de" → hints
  Spanish vs n-grams French), and Cyrillic input yields a uniform
  max-distance tie silently resolved to English (documented limitation).

### Changed

- In Auto mode the app's operational detector is now **char n-grams**
  (selectable; hint words stay available as the transparent baseline), and
  the JSON export records which detector produced the analysis
  (`"detector"`: `char_ngrams` / `hint_words` / `manual`).
- The char n-gram distance view is a ranked table (Rank / Language /
  Distance, lowest highlighted) instead of a bar chart, so a bigger bar can
  no longer be misread as a better match.
- Benchmark wording no longer suggests statistical equivalence with
  langdetect: the README states the absolute gap (one more error out of
  180) and `docs/benchmarks.md` now reports absolute error counts per
  system.

### Fixed

- App collocations were computed over the stopword-filtered token sequence,
  presenting non-adjacent pairs as adjacent bigrams; the default now uses
  the original token sequence (filtered mode remains as a clearly labeled
  option). The CLI was already correct.
- README was truncated mid-sentence in Non-goals and missing the newer
  methods and CLI commands from the catalog.
- `scripts/build_ngram_profiles.py` used `datetime.UTC` (Python 3.11+);
  now compatible with the supported 3.10 floor.

Planned (see [ROADMAP.md](ROADMAP.md) and [CONTENT_ROADMAP.md](CONTENT_ROADMAP.md)):
rest of the handbook, remaining lesson packages and videos, case-study
notebooks, instructor guide, lesson mode in the app.

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
