# ADR 0001 — MIT license

**Status:** accepted (2026-07-13)

**Context:** The repo shipped with an Unlicense LICENSE file while the
README claimed MIT — an inconsistency a reviewer spots in seconds.

**Decision:** MIT everywhere. It is the most widely recognized permissive
license, expected by employers and compatible with every resource we adapt
(spaCy stopwords are MIT; Gutenberg texts are public domain; UCI dataset is
CC BY 4.0, attribution given in evals/DATASETS.md).

**Consequences:** Attribution notices must be kept for adapted resources;
docs/resources.md is the single place where provenance lives.
