# ADR 0004 — Small frozen datasets checked into the repo

**Status:** accepted (2026-07-14)

**Context:** Evaluation needs licensed, reproducible gold data. Downloading
datasets at eval time makes results drift with upstream changes and breaks
offline reproducibility.

**Decision:** Check small frozen samples into `evals/datasets/` (180 langid
sentences, 120 sentiment sentences, 60 segmentation sentences), each with
documented source, license, sampling procedure and seed in
`evals/DATASETS.md`. Every result JSON records the dataset SHA-256, so a
benchmark number is tied to exact bytes.

**Consequences:** Datasets are deliberately small — big enough to rank
systems, small enough to inspect by hand; confidence intervals are wide and
that is documented. Growing them is a versioned change (new SHA-256, new
benchmark run).
