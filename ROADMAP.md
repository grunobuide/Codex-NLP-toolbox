# Roadmap

Engineering track. For what the toolbox should *contain* — resources, methods, and teaching material — see [CONTENT_ROADMAP.md](CONTENT_ROADMAP.md); the sequencing table there pairs content work with each phase below.

Target state: a repository where a technical reviewer can verify in under two minutes that the project is **installable, tested, measured against external baselines, and honest about its failure modes**.

Guiding principle: the NLP methods are intentionally simple; the value is the engineering shell around them — evaluation, reproducibility, and documented limitations. Scope stays fixed to the project statement: *a reproducible, evaluation-driven NLP toolbox for transparent linguistic baselines*.

## Phase 0 — Project contract ✅ (done)

MIT license, `pyproject.toml` + `uv.lock`, Python 3.10–3.13, runtime/dev dependency split, README repositioned with explicit non-goals.

## Phase 1 — Quality gates ✅ (pending first green run on GitHub)

Make every claim in the repo mechanically verified.

- [x] Ruff (lint + format), mypy on `nlp_toolbox/`, pytest with coverage floor.
- [x] Pre-commit hooks mirroring CI.
- [x] GitHub Actions: matrix on Python 3.10–3.13 — lint, type-check, tests, package build, and a clean-venv install smoke test (`pip install . && python -c "import nlp_toolbox"`).
- [x] `.gitattributes` for consistent line endings.
- [x] Badges in README: CI status, coverage, Python versions, license.
- [x] Housekeeping: move the Gutenberg sample text to `data/samples/` with provenance and license note.

**Visible outcome:** green CI badge; every PR gated by reproducible checks.

## Phase 2 — Library hardening + CLI (~1 week)

Make the toolbox usable outside the browser.

- [ ] API cleanup: remove unused parameters (e.g. `config` in `tokenize_text`), add docstrings with documented behavior for empty/edge inputs, type-complete public API.
- [ ] Make silent biases explicit: `detect_language` tie-breaking and English fallback become documented, testable behavior (e.g. return confidence/evidence, not just a label).
- [ ] CLI: `codex-nlp analyze <file> [--lang auto] [--json]` exposing the tool catalog with structured JSON output — usable in pipelines and scriptable for the eval harness.
- [ ] Entry point declared in `pyproject.toml`; CLI covered by tests.

**Visible outcome:** a reviewer can `uv run codex-nlp analyze data/samples/... --json` ten seconds after cloning.

## Phase 3 — Evaluation harness (~1–2 weeks)

The differentiator: stop asserting, start measuring.

- [ ] Separate `evals/` layer (not shipped in the wheel), with its own dependency group.
- [ ] Small, public, licensed datasets checked in with a `DATASETS.md` documenting source, license, and sampling procedure. Candidates: Tatoeba sentences (CC-BY) for language ID across the six supported languages; SST-2/IMDb subset for sentiment; UD English EWT (CC BY-SA) sentence boundaries for segmentation.
- [ ] Task definitions, metrics (accuracy, macro-F1, per-language confusion matrix), fixed seeds, run configs.
- [ ] Structured outputs: one JSON per run recording git SHA, dataset hash, config, and scores — reproducible by anyone.
- [ ] External baselines to beat/lose to, honestly reported: `langid`/`langdetect` (language ID), VADER (sentiment), `pysbd` or NLTK Punkt (segmentation).
- [ ] Results table auto-generated into `docs/benchmarks.md`.

**Visible outcome:** a benchmark table in the README comparing this toolbox against known baselines, with numbers a reviewer can reproduce with one command.

## Phase 4 — Error analysis (~1 week)

Document where the heuristics fail and why.

- [ ] Error taxonomy built from eval failures: short texts, code-switching, Unicode/emoji, malformed input, lexicon gaps, English-calibrated readability applied to other languages.
- [ ] Property-based tests (Hypothesis) for robustness invariants: no crashes on arbitrary Unicode, empty input contracts, tokenizer stability.
- [ ] Adversarial and ambiguous cases as regression fixtures.
- [ ] `docs/error-analysis.md`: expected vs observed behavior, root causes, and which failures are inherent to the method vs fixable.

**Visible outcome:** a limitations report that demonstrates measurement-driven engineering judgment — the rarest artifact in portfolio repos.

## Phase 5 — Public demo (~1 week)

- [ ] Deploy the Streamlit app to Hugging Face Spaces (free, serves Streamlit from the repo; also adds a public ML-community profile surface). Streamlit Community Cloud is the fallback.
- [ ] Add a **Benchmarks** tab to the app rendering the eval JSON outputs.
- [ ] Licensed sample texts per language, one-click loadable.
- [ ] Short GIF at the top of the README; exportable outputs (JSON/CSV) from the app.

**Visible outcome:** a live URL in the README and repo description — zero-setup proof it works.

## Phase 6 — Release & communication (~1 week)

- [ ] `v1.0.0` released to PyPI via GitHub Actions trusted publishing.
- [ ] `CHANGELOG.md` (Keep a Changelog format).
- [ ] `docs/architecture.md` plus 3–5 short ADRs recording real decisions (license, uv, eval design, why no ML dependencies).
- [ ] `CITATION.cff`.
- [ ] GitHub polish: repo description, topics, social preview image, pinned on profile.

**Visible outcome:** `pip install codex-nlp-toolbox` works; the repo reads as a maintained, versioned project.

## Definition of Done

- Reproducible install (lockfile + CI-verified on 3.10–3.13)
- Lint, typing, tests, and coverage gates on every PR
- Datasets with documented origin and license
- Quantitative results vs at least three external baselines
- Written error analysis and limitations
- Live demo
- Architecture docs and ADRs
- Versioned release on PyPI

## Explicit non-goals (unchanged)

No ML models, no agents, no microservices, no Kubernetes. This project competes on rigor, not scale.
