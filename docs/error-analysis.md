# Error analysis

Where the baselines fail, by how much, and why. Every number here comes
from a reproducible source: the eval confusion matrices
(`evals/results/*.json`), the robustness probes
(`uv run python -m evals.probes`), the property-based tests
(`tests/test_properties.py`) or the adversarial fixtures
(`tests/test_adversarial.py`). Nothing in this document is an anecdote.

## Language identification (hint-word method)

Headline: **75.6% accuracy** vs langdetect's 99.4% on 180 literary
sentences (`docs/benchmarks.md`).

### Failure mode 1 — zero evidence on short text (inherent, mitigable)

The detector only sees 6–7 function words per language. Short inputs often
contain none of them, triggering the documented English fallback:

| Input | Hint-words acc | Char-ngrams acc | Hint fallback rate |
|---|---|---|---|
| first 2 words | 0.2889 | 0.6111 | 77% |
| first 4 words | 0.4611 | 0.8111 | 51% |
| first 8 words | 0.5889 | 0.9111 | 28% |
| first 16 words | 0.7278 | 0.9889 | 11% |
| full sentence | 0.7556 | 0.9889 | 10% |

Root cause: evidence sparsity, not noise — accuracy tracks the fallback
rate almost exactly. The character n-gram detector (Cavnar–Trenkle) attacks precisely this —
character statistics exist in *every* token — and the table shows it
delivering: 98.9% on full sentences, matching langdetect within 0.6 points.

### Failure mode 2 — shared Romance hint words (structural)

From the confusion matrix (n=30 per language): fr→es 9, pt→es 6, es→fr 3,
it→es/pt 6. Cause: the hint lexicons overlap — *de* is a hint for Spanish,
French **and** Portuguese; *que* for three languages; *la* for three.
Overlapping evidence plus fixed-order tie-breaking systematically favors
languages earlier in `LANGUAGE_OPTIONS`. German, with no Romance overlap,
is only ever lost to the English fallback (de→en 6).

Fixable: disjoint hint sets, evidence weighting, or the n-gram detector.
The tie itself is visible to users (`detect_language_details.tied_with`).

### Failure mode 3 — non-Latin scripts (out of scope, documented)

Cyrillic/CJK input matches no hint and falls back to "English" with
`fallback=True` (pinned in `tests/test_adversarial.py`). The six-language
scope is declared in the README; the fallback flag is the honest signal.

## Sentiment (v1 lexicons)

Headline: **76.7% accuracy** vs VADER's 80.0% on 120 review sentences.

### Failure mode 1 — coverage gap (fixable: grow lexicons)

48% of test sentences contain **no** lexicon word at all; they default to
a negative prediction. Consequence, from the confusion matrix: negative
recall 52/60 (0.87) but positive recall only 40/60 (0.67) — positives that
express sentiment through domain vocabulary ("holds charge", "fries are
endless") are invisible. Lexicon size is the single highest-leverage fix,
and the eval harness can measure accuracy as a function of lexicon size
(planned case study).

### Failure mode 2 — negation blindness (inherent to bag-of-words)

"this is not good at all" scores *positive* (pinned in adversarial tests).
No lexicon fixes this; it needs at least a negation-window rule — a
teachable upgrade (VADER's rule set is the natural comparison).

### Failure mode 3 — morphology (fixable per language)

Exact lowercase matching misses inflected forms: German *schrecklicher*
missed until common adjective inflections were added to the lexicon
(v1 fix during Phase 3). Verb conjugations remain uncovered in all six
languages. A stemmer (planned: Porter for English) is the classic remedy —
with its own documented failure cases.

## Sentence segmentation (regex)

Headline: **F1 0.919** vs pysbd's 0.975 on UD-EWT web text.

- **Over-splitting on abbreviations** (precision 0.89): *Dr. Smith*,
  *U.S. President*, *Mrs. Tolchin* each produce a false boundary. Partially
  fixable with an abbreviation list — at the cost of the one-line
  transparency of the rule.
- **Under-splitting without terminal punctuation** (recall loss): newline-
  separated fragments stay glued. Inherent to punctuation-based rules.
- Decimals (*9.5%*, *3.14*) do **not** over-split: the rule requires
  whitespace after the period. Pinned in adversarial tests.

## Readability

The syllable estimator counts vowel groups with a silent-*e* rule applied
to English only. Diphthong/hiatus distinctions (*poeta*, *ciao*, *lied*)
are ignored in all languages, so per-language formulas receive slightly
biased syllable counts. Scores are only comparable within one language —
never across languages (different formulas, different scales).

## Crashes found and fixed

Property-based testing (Hypothesis, 200 arbitrary-Unicode examples per
invariant) found one real crash: `vocabulary_growth(step=0)` raised
`ZeroDivisionError`. Fixed with a documented `ValueError` contract and a
regression test. No public function crashes on arbitrary Unicode input
(`tests/test_properties.py` enforces this permanently).

## Summary: inherent vs fixable

| Failure | Verdict | Planned remedy |
|---|---|---|
| Language ID on short text | mitigated ✅ | char n-gram detector shipped (61% vs 29% on 2 words) |
| Romance hint overlap | fixed by alternative ✅ | n-gram detector: fr→es confusions eliminated |
| Non-Latin scripts | out of scope | explicit fallback flag (done) |
| Sentiment coverage gap | fixable | grow lexicons, measure vs size |
| Negation blindness | inherent to BoW | negation-window rule (teachable) |
| Morphology misses | partially fixable | Porter stemmer shipped (EN), failure cases pinned |
| Abbreviation over-split | partially fixable | abbreviation list (costs transparency) |
| Missing-punct under-split | inherent | document; compare with ML segmenters |
| Cross-language readability comparison | invalid by design | document (done) |
