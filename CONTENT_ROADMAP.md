# Content Roadmap

Companion to [ROADMAP.md](ROADMAP.md). That document makes the project *trustworthy*; this one makes it *useful* — and obviously so within the first minute of looking at it.

Primary audience: **NLP students and instructors**. All six supported languages (English, Spanish, French, German, Italian, Portuguese) are treated as first-class citizens.

Definition of useful: an instructor can run a lab session with zero preparation, and a student can trace every number the toolbox produces back to a formula, a lexicon entry, or a counting rule.

## Track 1 — Real linguistic resources

The current lexicons are placeholders (~15 stopwords per language, 30 English-only sentiment words, 6 hint words for detection). Usefulness starts with real, documented resources.

- [x] **Stopword lists**: 100–300 entries per language, adapted from spaCy 3.8 (MIT); 305–624 entries per language. Each list documented with source, size, and known gaps in `docs/resources.md`.
- [ ] **Sentiment lexicons for all six languages**: curated per-language lists (~200 entries each) with documented methodology and license. Lexicon size becomes a teachable variable — the eval harness (engineering roadmap, Phase 3) can show accuracy as a function of lexicon size.
- [x] **Language-specific readability formulas**, each with its academic citation: Flesch (EN), Fernández-Huerta (ES), Kandel-Moles (FR), Amstad (DE), Franchina-Vacca (IT), Martins adaptation (PT). Replaces the current English formula silently applied to every language.
- [ ] **Character n-gram language detection** (Cavnar–Trenkle) alongside the hint-word method: still fully interpretable, dramatically better on short texts, and a classic paper students should meet.

## Track 2 — Core-curriculum methods

New tools, chosen because they appear in every intro NLP syllabus and stay hand-inspectable:

- [ ] **TF-IDF keyword extraction** — presented side by side with raw frequency so students see *why* IDF matters.
- [ ] **Collocations** via PMI and log-likelihood ratio.
- [ ] **KWIC concordance** (keyword in context) — the classic corpus-linguistics view.
- [ ] **Zipf's law plot** (rank–frequency) and **vocabulary growth curve** — highly visual, one-slide teachable.
- [ ] **Porter stemmer** (English) as a worked example of rule-based normalization, with documented failure cases.
- [ ] **Text comparison mode**: load two texts side by side — two authors, two translations, two registers — and compare every metric. This is the killer classroom feature.

Every new method ships with: unit tests, a method card (what/how/why/explore), and an eval entry where a gold standard exists.

## Track 3 — The handbook

Method cards grow into a mini-handbook (`docs/handbook/`), one page per method:

- The formula and a **worked example computed by hand** on a five-word text — the number in the app must be reproducible on paper.
- Limitations and failure cases (fed by the error-analysis phase).
- Academic references and a pointer to the modern alternative (e.g. lexicon sentiment → VADER → transformers).

Plus **case studies** as runnable notebooks in `examples/` (Colab badge):

- [ ] *One novel, six languages* — Gutenberg translations of the same work compared on Zipf curves, lexical diversity, and readability.
- [ ] *How big must a sentiment lexicon be?* — accuracy vs lexicon size, using the eval harness.
- [ ] *Why language ID fails on short texts* — hint-word vs n-gram detection on tweets-length input.

## Track 4 — Making usefulness visible

- [ ] **Sample corpus pack**: short licensed texts for each of the six languages in `data/samples/`, one-click loadable in the app.
- [ ] **"Start here" tour** in the app: preloaded example with a guided reading of the results.
- [ ] README section **"Use this to…"** with three concrete scenarios and screenshots: teach a lab, profile a corpus, establish a baseline before modeling.
- [ ] **Instructor guide** (`docs/classroom.md`): a ready-to-use 90-minute lab plan with exercises and answers.

## Sequencing with the engineering roadmap

| Engineering phase | Content work that pairs with it |
|---|---|
| P1 Quality gates | Track 1 stopwords + readability formulas (small, testable) |
| P2 CLI | Track 2 TF-IDF, KWIC, Zipf (new API surface, CLI subcommands) |
| P3 Eval harness | Track 1 sentiment lexicons + n-gram detection (evals prove the upgrade) |
| P4 Error analysis | Track 3 handbook limitation sections |
| P5 Demo | Track 2 comparison mode + Track 4 tour, samples, screenshots |
| P6 Release | Track 3 case studies + Track 4 instructor guide |

## Quality bar

Every resource has provenance and license. Every method has a citation, a hand-computable example, and tests. Nothing ships that a student cannot verify with pencil and paper.
