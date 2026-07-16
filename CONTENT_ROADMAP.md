# Content Roadmap

Companion to [ROADMAP.md](ROADMAP.md). That document makes the project *trustworthy*; this one makes it *useful* — and obviously so within the first minute of looking at it.

Primary audience: **NLP students and instructors**. All six supported languages (English, Spanish, French, German, Italian, Portuguese) are treated as first-class citizens.

Definition of useful: an instructor can run a lab session with zero preparation, and a student can trace every number the toolbox produces back to a formula, a lexicon entry, or a counting rule.

## Track 1 — Real linguistic resources

The current lexicons are placeholders (~15 stopwords per language, 30 English-only sentiment words, 6 hint words for detection). Usefulness starts with real, documented resources.

- [x] **Stopword lists**: 100–300 entries per language, adapted from spaCy 3.8 (MIT); 305–624 entries per language. Each list documented with source, size, and known gaps in `docs/resources.md`.
- [x] **Sentiment lexicons for all six languages**: curated per-language lists (~200 entries each) with documented methodology and license. Lexicon size becomes a teachable variable — the eval harness (engineering roadmap, Phase 3) can show accuracy as a function of lexicon size.
- [x] **Language-specific readability formulas**, each with its academic citation: Flesch (EN), Fernández-Huerta (ES), Kandel-Moles (FR), Amstad (DE), Franchina-Vacca (IT), Martins adaptation (PT). Replaces the current English formula silently applied to every language.
- [x] **Character n-gram language detection** (Cavnar–Trenkle) alongside the hint-word method: still fully interpretable, dramatically better on short texts, and a classic paper students should meet.

## Track 2 — Core-curriculum methods

New tools, chosen because they appear in every intro NLP syllabus and stay hand-inspectable:

- [x] **TF-IDF keyword extraction** — presented side by side with raw frequency so students see *why* IDF matters.
- [x] **Collocations** via PMI and log-likelihood ratio.
- [x] **KWIC concordance** (keyword in context) — the classic corpus-linguistics view.
- [x] **Zipf's law plot** (rank–frequency) and **vocabulary growth curve** — highly visual, one-slide teachable.
- [x] **Porter stemmer** (English) as a worked example of rule-based normalization, with documented failure cases.
- [x] **Text comparison mode**: load two texts side by side — two authors, two translations, two registers — and compare every metric. This is the killer classroom feature.

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

- [x] **Sample corpus pack**: short licensed texts for each of the six languages in `data/samples/`, one-click loadable in the app.
- [ ] **"Start here" tour** in the app: preloaded example with a guided reading of the results.
- [ ] README section **"Use this to…"** with three concrete scenarios and screenshots: teach a lab, profile a corpus, establish a baseline before modeling.
- [ ] **Instructor guide** (`docs/classroom.md`): a ready-to-use 90-minute lab plan with exercises and answers.

## The course

The remaining content work is organized around a recorded course:
**"Fundamentos transparentes de PLN: do texto à avaliação"** — 7 lessons
of 15–30 min in Brazilian Portuguese, for Letters/Linguistics students, with
the live app as the on-screen material. Full syllabus and per-lesson
recording scripts: [docs/course/syllabus.md](docs/course/syllabus.md).
Editorial contract, pilot plan and open decisions:
[docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md](docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md).

### What "six first-class languages" means, precisely

| Layer | Coverage |
|---|---|
| Interface & didactic text | EN + PT-BR toggle (app), 6 analysis languages |
| Linguistic resources (stopwords, sentiment lexicons, readability formulas, n-gram profiles, samples) | all 6 languages, real parity |
| Evaluation | language ID: all 6 · sentiment & segmentation: **English only** (gold datasets) |
| Language-specific methods | Porter stemmer: **English only** |

Public promises (README, course) must distinguish these layers.

| # | Lesson (PT-BR) | App surface | Needs building |
|---|---|---|---|
| 1 | O texto como dados: tokens, sentenças, tipos e ocorrências | Analyze → Text structure | lesson preset |
| 2 | Leis estatísticas da língua: Zipf e crescimento do vocabulário | Analyze → Descriptive stats | notebook *One novel, six languages* |
| 3 | Palavras-chave e colocações: frequência, TF-IDF, KWIC, PMI | Analyze → Information extraction | (ready) |
| 4 | Que língua é essa? Evidência, empates e fallback | Analyze → Language profile | **pilot package** (see strategy doc) |
| 5 | Sentimento com dicionários: léxicos, morfologia e negação | Analyze → Sentiment | lexicon-size notebook |
| 6 | Legibilidade e estilo: fórmulas por língua, comparação de traduções | Compare two texts | (ready) |
| 7 | Como saber se funciona? Ouro, métricas e análise de erros | Benchmarks | (ready — the signature lesson) |

All seven lessons are now recordable content-wise; what remains is the
production system (presets, exercises, notebooks) — built pilot-first.

### Course phases

Revised 2026-07-16 (see the strategy doc for rationale): validate one full
lesson before mass-producing seven.

- [x] **C1 — Missing methods** ✅ (2026-07-14): character n-gram detection
  (Cavnar–Trenkle) with eval entry proving the upgrade over hint-words;
  collocations via PMI and log-likelihood; Porter stemmer with documented
  failure cases. Each with tests, method card, CLI subcommand.
- [x] **C2 — Bilingual didactic layer** ✅ (2026-07-15): EN/PT-BR toggle for
  the app's didactic strings (`app_i18n.py`, key-parity tests) — code and
  API stay in English; the recorded screen reads in Portuguese.
- [x] **C2.1 — Content QA** ✅ (2026-07-16): syllabus aligned with the app
  (lesson 2 corpus roles, lesson 5 English-only Porter examples, no fixed
  numbers in scripts), `language_hint_evidence` API so the lesson-4 promise
  ("which words decided") is literally true, language-coverage matrix above.
- [x] **C2.2 — Editorial contract** ✅ (2026-07-16):
  [docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md](docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md)
  — audience, promise, title, format, language policy, CTA hierarchy,
  success metrics; open decisions tracked there (channel, weekly cadence).
- [ ] **C3 — Vertical slice (pilot: lesson 4)**: one complete lesson, app to
  video. Done: first handbook page
  ([docs/handbook/deteccao-de-idioma.md](docs/handbook/deteccao-de-idioma.md)),
  versioned preset with test-pinned expected results
  ([docs/course/aula-04/preset.md](docs/course/aula-04/preset.md),
  `tests/test_lesson_presets.py`), exercises + commented answer key
  ([docs/course/aula-04/exercicios.md](docs/course/aula-04/exercicios.md)).
  Remaining: lesson page, video (blocked on channel decision), optional
  notebook, one short derived piece. Validates format before scaling.
- [ ] **C4 — Content system**: templates, glossary, preset conventions and
  per-lesson contract distilled from the pilot's lessons learned.
- [ ] **C5 — First season**: the seven lessons and their essential materials
  (production order 4 → 7 → 1 → 3 → 2 → 5 → 6; publication order 1–7).
- [ ] **C6 — Expansion**: advanced notebooks, workshops, derived content,
  instructor guide, lesson mode in the app.

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
