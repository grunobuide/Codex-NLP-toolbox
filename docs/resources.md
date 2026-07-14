# Linguistic resources: provenance and limitations

Every packaged resource lists its source, license, size, and known gaps. If a
resource is not listed here, it should not be in the package.

## Stopword lists (`nlp_toolbox/resources/stopwords/`)

Extracted from the `spacy.lang.<code>.stop_words` modules of
[spaCy](https://github.com/explosion/spaCy) **3.8.14** (MIT license),
deduplicated and sorted, one word per line, UTF-8, lowercase.

| File | Language | Entries |
|---|---|---|
| `en.txt` | English | 305 |
| `es.txt` | Spanish | 521 |
| `fr.txt` | French | 507 |
| `de.txt` | German | 543 |
| `it.txt` | Italian | 624 |
| `pt.txt` | Portuguese | 416 |

Known limitations:

- Lists are general-purpose; domain texts (legal, medical, social media) need
  domain-specific additions.
- Matching is exact and lowercase: tokens must be lowercased first, and no
  lemmatization is applied (`é`/`e` in Portuguese/Italian are distinct entries).
- List sizes differ by language, so cross-language comparisons of
  stopword-filtered counts are not size-normalized.
- German nouns are capitalized in running text; the lowercase-matching caveat
  matters most there.

## Language detection hints (`languages.LANGUAGE_HINTS`)

Hand-picked sets of 6–7 very high-frequency function words per language,
chosen so the per-language evidence table in the app stays readable. This is
a deliberately weak, fully transparent detector: it fails on short texts and
between closely related languages (Spanish/Portuguese). A character n-gram
detector (Cavnar–Trenkle 1994) is planned as the stronger interpretable
alternative — see CONTENT_ROADMAP Track 1.

## Sentiment word lists (`tools.POSITIVE_WORDS` / `tools.NEGATIVE_WORDS`)

Hand-curated English seed lists (~15 words each). **Placeholder status**:
English-only, tiny, and unweighted. Replacement with documented per-language
lexicons is scheduled with the evaluation harness (engineering roadmap
Phase 3), so the upgrade lands together with the measurement that proves it.
