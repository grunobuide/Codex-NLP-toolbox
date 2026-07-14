# Evaluation datasets: provenance and sampling

Frozen TSV files are the canonical evaluation sets. They are small by design:
big enough to rank systems honestly, small enough to inspect by hand.

## `langid.tsv` — language identification (180 sentences, 30 per language)

Tab-separated: `label<TAB>text`. Labels: `en es fr de it pt`.

Source: one public-domain novel per language from Project Gutenberg
(Gutenberg license; the ebooks are public domain in the USA):

| Label | Work | Author | PG # |
|---|---|---|---|
| en | Frankenstein | Mary Shelley | 84 |
| es | Don Quijote | Miguel de Cervantes | 2000 |
| fr | Candide, ou l'optimisme | Voltaire | 4650 |
| de | Die Verwandlung | Franz Kafka | 22367 |
| it | I promessi sposi | Alessandro Manzoni | 45334 |
| pt | Dom Casmurro | Machado de Assis | 55752 |

Sampling procedure (2026-07-14): Gutenberg header/footer stripped
(`*** START`/`*** END` markers); text whitespace-normalized and split on
`(?<=[.!?])\s+`; sentences kept if 40–140 chars, starting with an uppercase
letter, ending in `.!?`, and containing no digits, brackets, underscores or
guillemets; deduplicated; 30 sampled per language with a seeded shuffle
(seed 42; LCG in-browser for es/fr/de/it/pt, Python `random` for en).
The frozen TSV is canonical — rerunning the procedure is not required to
reproduce any benchmark number.

Known biases: 19th/18th-century literary register; Dom Casmurro uses
pre-1943 Portuguese orthography; one single work per language (no domain
variety). See `docs/error-analysis.md` (planned) for the consequences.

## `sentiment_en.tsv` — binary sentiment, English (120 sentences, 60/60)

Tab-separated: `label<TAB>source<TAB>text`. Labels: `1` positive, `0` negative.

Source: "From Group to Individual Labels using Deep Features"
(Kotzias et al., KDD 2015) — *Sentiment Labelled Sentences*, UCI Machine
Learning Repository, dataset #331, CC BY 4.0.
40 sentences per source (amazon, imdb, yelp), balanced 20 positive /
20 negative per source, max length 90 chars, seeded shuffle (seed 42).

Known biases: English only; product/restaurant/movie review register; short
sentences. The multilingual gap of the toolbox's lexicons is documented in
`docs/resources.md` and will be measured when multilingual labeled sets are
added.

## `segmentation_en.txt` — sentence segmentation gold, English (60 sentences)

One gold sentence per line. Source: `# text =` annotations of the **test**
split of [UD English EWT](https://github.com/UniversalDependencies/UD_English-EWT)
(Universal Dependencies, CC BY-SA 4.0) — web text: reviews, emails, forums.
Filtered to 40–120 chars ending in `.!?`; deduplicated; 60 sampled with a
seeded shuffle (seed 42, LCG). At eval time sentences are joined into
deterministic paragraphs of 3 (single spaces) and systems must recover the
originals; scoring is exact-match multiset precision/recall/F1.

Known biases: English only; contains abbreviation traps (Dr., Mrs., U.S.,
W., '71) which is precisely why UD web text was chosen over literary prose.
