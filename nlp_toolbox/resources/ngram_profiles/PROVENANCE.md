# Character n-gram profiles — provenance and licensing

The files `en.txt`, `es.txt`, `fr.txt`, `de.txt`, `it.txt`, `pt.txt` are ranked
top-300 character-trigram profiles used by the Cavnar–Trenkle (1994) language
detector (`nlp_toolbox.tools.detect_language_ngram_details`). They are **derived
works of Wikipedia article text** and are therefore licensed **CC BY-SA 4.0**,
*not* under the repository's MIT license. See the top-level [`NOTICE`](../../../NOTICE).

## Method

Top-300 character trigrams per language, in rank order, one per line, UTF-8.
Normalization (identical to detection time, `build_ngram_profile`): text is
lowercased, every run of non-letter characters is collapsed to a single `_`
word-boundary marker, and trigrams containing at least one letter are counted
and ranked by frequency (ties broken alphabetically). Reference: Cavnar, W. B.
& Trenkle, J. M. (1994), *N-gram-based text categorization*, SDAIR-94.

## Sources

For each language, the training text is the concatenation of the plain-text
extracts of three articles from **that language's own Wikipedia**: the article
about the language itself, plus *Literature* and *Linguistics* in that language.

| Language | Wikipedia | Articles (canonical titles) |
|---|---|---|
| English | en.wikipedia.org | [English language](https://en.wikipedia.org/wiki/English_language), [Literature](https://en.wikipedia.org/wiki/Literature), [Linguistics](https://en.wikipedia.org/wiki/Linguistics) |
| Spanish | es.wikipedia.org | [Idioma español](https://es.wikipedia.org/wiki/Idioma_espa%C3%B1ol), [Literatura](https://es.wikipedia.org/wiki/Literatura), [Lingüística](https://es.wikipedia.org/wiki/Ling%C3%BC%C3%ADstica) |
| French | fr.wikipedia.org | [Français](https://fr.wikipedia.org/wiki/Fran%C3%A7ais), [Littérature](https://fr.wikipedia.org/wiki/Litt%C3%A9rature), [Linguistique](https://fr.wikipedia.org/wiki/Linguistique) |
| German | de.wikipedia.org | [Deutsche Sprache](https://de.wikipedia.org/wiki/Deutsche_Sprache), [Literatur](https://de.wikipedia.org/wiki/Literatur), [Sprachwissenschaft](https://de.wikipedia.org/wiki/Sprachwissenschaft) |
| Italian | it.wikipedia.org | [Lingua italiana](https://it.wikipedia.org/wiki/Lingua_italiana), [Letteratura](https://it.wikipedia.org/wiki/Letteratura), [Linguistica](https://it.wikipedia.org/wiki/Linguistica) |
| Portuguese | pt.wikipedia.org | [Língua portuguesa](https://pt.wikipedia.org/wiki/L%C3%ADngua_portuguesa), [Literatura](https://pt.wikipedia.org/wiki/Literatura), [Linguística](https://pt.wikipedia.org/wiki/Lingu%C3%ADstica) |

## Reproducing the profiles

The build is scripted and deterministic given a fixed set of article revisions:

```bash
python -m scripts.build_ngram_profiles          # fetch + rebuild all profiles
python -m scripts.build_ngram_profiles --check  # dry run: print provenance only
```

The script fetches article text and revision metadata through the MediaWiki API
(`action=query&prop=extracts|revisions`), rebuilds each profile with the exact
detection-time normalization, and writes `manifest.json` next to the profiles
with, per article, the resolved **title, URL, revision id, and revision
timestamp**, plus the **SHA-256** of each generated profile file and the UTC
build timestamp.

## Frozen build and revision note

The profiles currently shipped were built on **2026-07-14**. The original build
did **not** record per-article revision ids, so this snapshot documents the
stable article identities (titles and URLs) rather than exact revisions. Running
`scripts/build_ngram_profiles.py` regenerates the profiles from the *current*
Wikipedia revisions and writes a complete `manifest.json` (including revision
ids) — because Wikipedia content changes over time, the regenerated profiles may
differ slightly from the frozen files. Treat any regeneration as a deliberate,
versioned change: commit the new profiles together with the manifest and re-run
the evaluation harness (`docs/benchmarks.md`).

## Attribution

Text of the articles listed above © their respective Wikipedia contributors,
licensed CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). These
profiles are a derivative statistical summary (character-trigram frequency
rankings) of that text and are redistributed under the same license.
