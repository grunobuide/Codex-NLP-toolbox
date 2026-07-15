# Architecture

One package, one app, one eval layer. The structure mirrors the project
statement: transparent baselines (library), inspectable behavior (app),
measured claims (evals).

```
nlp_toolbox/            The shipped library (pure stdlib at runtime)
├── tools.py            All baseline methods; every function hand-traceable
├── languages.py        Language configs + cached resource loaders
├── resources/          Packaged data: stopwords/, sentiment/ (provenance
│                       in docs/resources.md)
└── cli.py              argparse CLI (codex-nlp), stable --json output

app.py                  Streamlit UI: Analyze / Compare / Benchmarks modes;
                        imports only the public library API

evals/                  NOT shipped in the wheel; own dependency group
├── datasets/           Frozen TSV/TXT gold data (evals/DATASETS.md)
├── metrics.py          Hand-implemented accuracy, macro-F1, confusion, PRF
├── run.py              Task runners -> results/*.json (git SHA + data hash)
├── probes.py           Robustness probes (degraded-input measurements)
└── report.py           results/*.json -> docs/benchmarks.md

tests/                  Unit + property-based (Hypothesis) + adversarial
                        regression fixtures; coverage floor 90%
.github/workflows/      ci.yml (matrix 3.10-3.13), release.yml (PyPI OIDC),
                        hf-space.yml (optional mirror, gated)
```

## Data flow

Text → `tokenize_text` / `split_sentences` → counting/lexicon methods →
dicts of plain Python values. No global state except two `@cache`d resource
loaders. The CLI and the app are thin views over the same functions the
evals measure — there is exactly one implementation of every method.

## Design principles

1. **Pencil-and-paper verifiability.** Every shipped number must be
   recomputable by hand: no ML dependencies in the runtime package, metrics
   implemented from scratch, formulas documented with citations.
2. **Degrade, don't raise.** Unsupported languages yield empty resource
   sets and zero scores; empty input yields empty output. Contracts are in
   docstrings and enforced by property tests.
3. **Biases must be visible.** Where a heuristic has a bias (English
   fallback, tie-breaking order, no negation handling) the API exposes it
   (`LanguageDetection.fallback`/`tied_with`) and the error analysis
   measures it.
4. **Evidence over claims.** Anything the README asserts about quality
   links to a benchmark table or an error-analysis section that a reviewer
   can reproduce with one command.

Decision records: [docs/adr/](adr/).
