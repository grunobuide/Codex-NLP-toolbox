# Roadmap

> **Status (2026-07-16): all engineering phases below are complete** (v1.1.0).
> The project is stable and in maintenance; active work continues on the
> content track ([CONTENT_ROADMAP.md](CONTENT_ROADMAP.md)), currently paused
> mid-pilot with open decisions documented in the
> [strategy doc](docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md).
> To pick the project up: [CONTRIBUTING.md](CONTRIBUTING.md).

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

## Phase 2 — Library hardening + CLI ✅

Make the toolbox usable outside the browser.

- [x] API cleanup: remove unused parameters (e.g. `config` in `tokenize_text`), add docstrings with documented behavior for empty/edge inputs, type-complete public API.
- [x] Make silent biases explicit: `detect_language` tie-breaking and English fallback become documented, testable behavior (e.g. return confidence/evidence, not just a label).
- [x] CLI: `codex-nlp analyze <file> [--lang auto] [--json]` exposing the tool catalog with structured JSON output — usable in pipelines and scriptable for the eval harness.
- [x] Entry point declared in `pyproject.toml`; CLI covered by tests.

**Visible outcome:** a reviewer can `uv run codex-nlp analyze data/samples/... --json` ten seconds after cloning.

## Phase 3 — Evaluation harness ✅

The differentiator: stop asserting, start measuring.

- [x] Separate `evals/` layer (not shipped in the wheel), with its own dependency group.
- [x] Small, public, licensed datasets checked in with a `DATASETS.md` documenting source, license, and sampling procedure. Candidates: Tatoeba sentences (CC-BY) for language ID across the six supported languages; SST-2/IMDb subset for sentiment; UD English EWT (CC BY-SA) sentence boundaries for segmentation.
- [x] Task definitions, metrics (accuracy, macro-F1, per-language confusion matrix), fixed seeds, run configs.
- [x] Structured outputs: one JSON per run recording git SHA, dataset hash, config, and scores — reproducible by anyone.
- [x] External baselines to beat/lose to, honestly reported: `langdetect` (language ID), VADER (sentiment). Segmentation vs `pysbd` added in Phase 4 (UD-EWT gold).
- [x] Results table auto-generated into `docs/benchmarks.md`.

**Visible outcome:** a benchmark table in the README comparing this toolbox against known baselines, with numbers a reviewer can reproduce with one command.

## Phase 4 — Error analysis ✅

Document where the heuristics fail and why.

- [x] Error taxonomy built from eval failures: short texts, code-switching, Unicode/emoji, malformed input, lexicon gaps, English-calibrated readability applied to other languages.
- [x] Property-based tests (Hypothesis) for robustness invariants: no crashes on arbitrary Unicode, empty input contracts, tokenizer stability.
- [x] Adversarial and ambiguous cases as regression fixtures.
- [x] `docs/error-analysis.md`: expected vs observed behavior, root causes, and which failures are inherent to the method vs fixable.

**Visible outcome:** a limitations report that demonstrates measurement-driven engineering judgment — the rarest artifact in portfolio repos.

## Phase 5 — Public demo ✅

- [x] Public demo on Streamlit Community Cloud (HF Spaces now requires a paid tier for Docker, and the native Streamlit SDK was deprecated). `requirements.txt` is the Cloud deployment manifest; a HF Spaces sync workflow (`hf-space.yml`) remains available, gated on the `HF_SPACE` variable, if a Docker Space becomes viable later.
- [x] Add a **Benchmarks** tab to the app rendering the eval JSON outputs.
- [x] Licensed sample texts per language, one-click loadable.
- [x] Short GIF at the top of the README (recorded from the live app). Exportable JSON from the app: done.

**Visible outcome:** a live URL in the README and repo description — zero-setup proof it works.

## Phase 6 — Release & communication (~1 week)

- [x] Release pipeline ready: `release.yml` publishes on `v*` tags via PyPI trusted publishing (OIDC), gated on the full test suite. First release pending the one-time PyPI publisher setup + tag.
- [x] `CHANGELOG.md` (Keep a Changelog format), v1.0.0.
- [x] `docs/architecture.md` plus 5 ADRs (license, uv/PEP 621, no-ML runtime, frozen datasets, Streamlit Cloud deploy).
- [x] `CITATION.cff`.
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
