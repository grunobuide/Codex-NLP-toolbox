# Contributing / picking this project up

This file is the map for anyone (including future-me) resuming work here.
The project is intentionally paused in a clean state: nothing is
half-broken, and every open decision is written down where you'd look for it.

## Orientation — where things are decided

| Question | Source of truth |
|---|---|
| What the project is / is not | [README.md](README.md) (positioning, non-goals, status) |
| Engineering plan (done) | [ROADMAP.md](ROADMAP.md) — phases 0–6, all complete |
| Content/course plan (paused mid-C3) | [CONTENT_ROADMAP.md](CONTENT_ROADMAP.md) |
| Editorial decisions + open questions | [docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md](docs/Codex_NLP_Content_Strategy_and_Pilot_Decisions.md) |
| Why key choices were made | [docs/adr/](docs/adr/) + [docs/architecture.md](docs/architecture.md) |
| Resource provenance & licensing | [docs/resources.md](docs/resources.md), [NOTICE](NOTICE), `nlp_toolbox/resources/ngram_profiles/PROVENANCE.md` |
| Measured performance & failures | [docs/benchmarks.md](docs/benchmarks.md), [docs/error-analysis.md](docs/error-analysis.md) |

## Development setup

```bash
git clone https://github.com/grunobuide/Codex-NLP-toolbox.git
cd Codex-NLP-toolbox
uv sync --group dev        # reproducible install from uv.lock
uv run pre-commit install  # hooks mirror CI
```

## Quality gates (all must pass before any commit)

```bash
uv run ruff check .   # lint; app_i18n.py is exempt from E501 only (translation data)
uv run mypy           # strict, scoped to nlp_toolbox/ via pyproject — do NOT run `mypy .`
uv run pytest         # 112 tests, coverage floor 90% on nlp_toolbox/
```

CI runs the same three on Python 3.10–3.13 plus a wheel install smoke test.
Notes that save you time:

- `mypy .` will fail on `.venv` and the optional `evals/` deps — the
  project intentionally scopes mypy with `files = ["nlp_toolbox"]`.
- `tests/test_i18n.py` enforces EN/PT key parity: adding any user-facing
  string to `app_i18n.py` requires both languages (the test tells you
  what's missing).
- `tests/test_lesson_presets.py` pins every number quoted in the course
  materials (`docs/course/`). If your change breaks one of these, either
  your change is a bug or you must update the lesson docs in the same
  commit. Never let recorded numbers drift silently.

## Running the evaluation harness

```bash
uv sync --group evals
uv run python -m evals.run --task <langid|sentiment|segmentation>
uv run python -m evals.report        # regenerates docs/benchmarks.md — never edit it by hand
```

Datasets are frozen with SHA-256 provenance (`evals/DATASETS.md`). If you
regenerate the char n-gram profiles (`python -m scripts.build_ngram_profiles`),
treat it as a versioned change: commit the new profiles + `manifest.json`
together, re-run the evals, and update `tests/test_lesson_presets.py` pins.

## Conventions

- **Code, APIs, tool names, JSON keys: English.** On-screen didactic text:
  bilingual via `app_i18n.py` (EN + PT-BR).
- Every packaged resource needs provenance + license in `docs/resources.md`
  (and `NOTICE` if the license differs from MIT).
- Every method ships with: tests, a method card (`app_i18n.TOOL_CARDS`),
  a CLI subcommand where it makes sense, and an eval entry where a gold
  standard exists.
- Quality bar for course material: every number verifiable with pencil and
  paper, and pinned by a test.

## Where to resume

**Engineering**: nothing pending. Candidate improvements are listed in
`docs/error-analysis.md` (e.g., the char n-gram detector returns English on
a uniform max-distance tie — Cyrillic input — without a fallback flag; see
`tests/test_lesson_presets.py::test_russo_ngram_max_distance_tie`).

**Content** (the actual frontier): phase C3 in
[CONTENT_ROADMAP.md](CONTENT_ROADMAP.md). The lesson-4 pilot package is
done (handbook page, preset, exercises — all test-pinned). Remaining, in
order:

1. Decide the publishing channel (platform / YouTube) — blocks the video.
2. Record the pilot video using [docs/course/aula-04/preset.md](docs/course/aula-04/preset.md).
3. Lesson page + optional notebook + one short derived piece.
4. Validate with real students (checklist in the strategy doc), then
   template the format (C4) and produce the season (C5).

**Optional release step**: PyPI trusted publishing was configured for the
`release.yml` workflow but may never have been activated on pypi.org. To
publish: pypi.org → Publishing → add pending publisher (project
`codex-nlp-toolbox`, owner `grunobuide`, repo `Codex-NLP-toolbox`, workflow
`release.yml`, environment `pypi`), create the matching GitHub environment,
then `git tag v1.1.0 && git push --tags`. The workflow gates on tests and
checks tag == `pyproject.toml` version. This is optional — the project is
fully usable from source and the live demo.
