# ADR 0003 — No ML dependencies in the runtime package

**Status:** accepted (2026-07-13)

**Context:** Adding spaCy/NLTK/transformers would improve accuracy but the
project's value proposition is *transparent baselines*: methods a student
can verify with pencil and paper and an engineer can use as the floor to
beat.

**Decision:** The shipped package uses only the standard library (plus
streamlit for the UI). Stronger systems (langdetect, VADER, pysbd) appear
only in the `evals` dependency group — as measurement baselines, not
features.

**Consequences:** The toolbox will lose to specialized systems by design;
docs/benchmarks.md quantifies the gap and docs/error-analysis.md explains
it. Accuracy improvements must come from better interpretable resources
(bigger lexicons, n-gram profiles), never from opaque models.
