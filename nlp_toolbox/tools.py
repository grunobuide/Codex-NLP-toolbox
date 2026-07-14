"""Core NLP baselines: counting, regex, and lexicon methods.

Every function is a transparent baseline — its output can be reproduced by
hand. See ``docs/handbook/`` (planned) for worked examples and
``docs/resources.md`` for lexicon provenance.
"""

import re
from collections import Counter
from math import log10
from typing import NamedTuple

from nlp_toolbox.languages import (
    LANGUAGE_OPTIONS,
    LanguageConfig,
    get_language_config,
    load_sentiment_lexicon,
)

WORD_PATTERN = re.compile(r"[\w']+", re.UNICODE)
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")

_VOWELS = "aeiouyáéíóúàèìòùâêîôûäëïöüãõœæ"


class ReadabilityFormula(NamedTuple):
    """Coefficients and citation for a language-specific readability formula.

    All supported formulas share the shape::

        score = base - wps_coefficient * words_per_sentence
                     - spw_coefficient * syllables_per_word
    """

    name: str
    base: float
    wps_coefficient: float
    spw_coefficient: float
    reference: str


READABILITY_FORMULAS: dict[str, ReadabilityFormula] = {
    "English": ReadabilityFormula(
        "Flesch Reading Ease",
        206.835,
        1.015,
        84.6,
        "Flesch, R. (1948). A new readability yardstick. J. Applied Psychology, 32(3).",
    ),
    "Spanish": ReadabilityFormula(
        "Fernández Huerta",
        206.84,
        1.02,
        60.0,
        "Fernández Huerta, J. (1959). Medidas sencillas de lecturabilidad. Consigna, 214.",
    ),
    "French": ReadabilityFormula(
        "Kandel–Moles",
        207.0,
        1.015,
        73.6,
        "Kandel, L., & Moles, A. (1958). Application de l'indice de Flesch à la langue "
        "française. Cahiers Études de Radio-Télévision, 19.",
    ),
    "German": ReadabilityFormula(
        "Amstad",
        180.0,
        1.0,
        58.5,
        "Amstad, T. (1978). Wie verständlich sind unsere Zeitungen? University of Zurich.",
    ),
    "Italian": ReadabilityFormula(
        "Franchina–Vacca",
        217.0,
        1.3,
        60.0,
        "Franchina, V., & Vacca, R. (1986). Adaptation of Flesch readability index "
        "on a bilingual text. Linguaggi, 3.",
    ),
    "Portuguese": ReadabilityFormula(
        "Flesch adaptado (Martins et al.)",
        248.835,
        1.015,
        84.6,
        "Martins, T. B. F., et al. (1996). Readability formulas applied to textbooks "
        "in Brazilian Portuguese (ICMC-USP Technical Report 28).",
    ),
}


def analyze_text(text: str, tokens: list[str], sentences: list[str]) -> dict[str, float | int]:
    """Compute count-based summary statistics for ``text``.

    Averages are guarded against empty inputs (denominator floored at 1), so
    empty text yields zeros rather than errors.
    """
    average_word_length = round(sum(len(token) for token in tokens) / max(len(tokens), 1), 2)
    average_sentence_length = round(len(tokens) / max(len(sentences), 1), 2)
    unique_words = len(set(tokens))
    lexical_diversity = round(unique_words / max(len(tokens), 1), 3)
    reading_time_min = round(len(tokens) / 200, 2)
    return {
        "characters": len(text),
        "words": len(tokens),
        "sentences": len(sentences),
        "avg_word_length": average_word_length,
        "avg_sentence_length": average_sentence_length,
        "unique_words": unique_words,
        "lexical_diversity": lexical_diversity,
        "estimated_reading_time_min": reading_time_min,
    }


def split_sentences(text: str) -> list[str]:
    """Split ``text`` into sentences on whitespace after ``.``, ``!`` or ``?``.

    A deliberately simple rule: it over-splits on abbreviations ("Dr. Smith")
    and under-splits when punctuation is missing. Whitespace-only input
    returns an empty list.
    """
    text = text.strip()
    if not text:
        return []
    sentences = SENTENCE_PATTERN.split(text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def tokenize_text(text: str, lowercase: bool = True) -> list[str]:
    """Extract word-like tokens (Unicode word characters and apostrophes)."""
    tokens = [match.group(0) for match in WORD_PATTERN.finditer(text)]
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens


def filter_tokens(
    tokens: list[str],
    config: LanguageConfig,
    remove_stopwords: bool = True,
    min_length: int = 1,
) -> list[str]:
    """Drop stopwords (per ``config``) and tokens shorter than ``min_length``.

    Matching is exact and case-sensitive: lowercase the tokens first
    (``tokenize_text`` does this by default).
    """
    stopwords = config["stopwords"] if remove_stopwords else set()
    return [token for token in tokens if token not in stopwords and len(token) >= min_length]


def generate_ngrams(tokens: list[str], n: int) -> list[str]:
    """Return contiguous ``n``-token windows joined by single spaces."""
    if n <= 1:
        return tokens
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def extract_keywords(
    tokens: list[str], config: LanguageConfig, top_k: int = 10
) -> list[dict[str, str | int]]:
    """Rank non-stopword tokens by raw frequency (top ``top_k``)."""
    filtered = filter_tokens(tokens, config, remove_stopwords=True, min_length=1)
    frequencies = Counter(filtered).most_common(top_k)
    return [{"term": term, "count": count} for term, count in frequencies]


def top_ngrams(tokens: list[str], n: int, top_k: int = 10) -> list[dict[str, str | int]]:
    """Rank ``n``-grams by frequency (top ``top_k``)."""
    ngrams = generate_ngrams(tokens, n)
    frequencies = Counter(ngrams).most_common(top_k)
    return [{"ngram": term, "count": count} for term, count in frequencies]


def readability_score(
    text: str,
    tokens: list[str],
    sentences: list[str],
    language: str = "English",
) -> float:
    """Language-calibrated readability score (higher = easier).

    Applies the formula registered for ``language`` in
    ``READABILITY_FORMULAS`` (Flesch for English, Fernández Huerta for
    Spanish, Kandel–Moles for French, Amstad for German, Franchina–Vacca for
    Italian, Martins et al. for Portuguese). Unknown languages fall back to
    the English Flesch formula. Scores are only comparable within one
    language. Returns 0.0 for empty input.
    """
    if not tokens or not sentences:
        return 0.0
    formula = READABILITY_FORMULAS.get(language, READABILITY_FORMULAS["English"])
    syllables = sum(_estimate_syllables(token, language) for token in tokens)
    words_per_sentence = len(tokens) / max(len(sentences), 1)
    syllables_per_word = syllables / max(len(tokens), 1)
    score = (
        formula.base
        - formula.wps_coefficient * words_per_sentence
        - formula.spw_coefficient * syllables_per_word
    )
    return round(score, 2)


def sentiment_analysis(tokens: list[str], language: str = "English") -> dict[str, float]:
    """Count lexicon hits per polarity; score = (pos − neg) / tokens.

    Uses the hand-curated seed lexicon for ``language`` (v1, ~75–100 words
    per polarity; see ``docs/resources.md``). No negation or intensifier
    handling — "not good" counts as positive. That failure mode is measured
    in ``docs/benchmarks.md`` and documented rather than hidden. Tokens must
    be lowercase. Unsupported languages score 0 on everything.
    """
    positive_words, negative_words = load_sentiment_lexicon(language)
    positive = sum(1 for token in tokens if token in positive_words)
    negative = sum(1 for token in tokens if token in negative_words)
    total = max(len(tokens), 1)
    score = round((positive - negative) / total, 3)
    return {
        "positive": positive,
        "negative": negative,
        "score": score,
    }


def word_length_distribution(tokens: list[str]) -> dict[int, int]:
    """Histogram of token lengths (characters), sorted by length."""
    lengths = Counter(len(token) for token in tokens)
    return dict(sorted(lengths.items(), key=lambda item: item[0]))


def language_hint_hits(tokens: list[str]) -> dict[str, int]:
    """Count, per language, how many tokens appear in its hint-word set."""
    scores = {}
    for language in LANGUAGE_OPTIONS:
        config = get_language_config(language)
        hints = config["hints"]
        scores[language] = sum(1 for token in tokens if token in hints)
    return scores


class LanguageDetection(NamedTuple):
    """Outcome of hint-word language detection, with its full evidence.

    ``fallback`` is True when no hint word matched and English was returned
    by convention. ``tied_with`` lists other languages with the same top
    score; ties are resolved by ``LANGUAGE_OPTIONS`` order. Both conditions
    are explicit here precisely because they are silent biases otherwise.
    """

    language: str
    scores: dict[str, int]
    tied_with: list[str]
    fallback: bool


def detect_language_details(text: str) -> LanguageDetection:
    """Detect the language of ``text`` and return the evidence behind the pick.

    Scores each supported language by counting tokens found in its hint-word
    set (``language_hint_hits``). Zero evidence anywhere yields English with
    ``fallback=True``.
    """
    tokens = tokenize_text(text)
    scores = language_hint_hits(tokens)
    best_language = max(scores, key=lambda lang: scores[lang])
    best_score = scores[best_language]
    if best_score == 0:
        return LanguageDetection("English", scores, [], True)
    tied_with = [
        lang for lang, score in scores.items() if score == best_score and lang != best_language
    ]
    return LanguageDetection(best_language, scores, tied_with, False)


def detect_language(text: str) -> str:
    """Pick the language whose hint words appear most often in ``text``.

    Convenience wrapper over ``detect_language_details``; use that function
    to inspect scores, ties, and the English fallback explicitly.
    """
    return detect_language_details(text).language


def tfidf_keywords(documents: list[list[str]], top_k: int = 10) -> list[dict[str, str | float]]:
    """Rank terms by TF-IDF across ``documents`` (each a token list).

    For term ``t``: ``tfidf(t) = tf(t) * log10(N / df(t))`` where ``tf`` is
    the total count over all documents, ``N`` the number of documents, and
    ``df`` the number of documents containing ``t``. With a single document
    every idf is ``log10(1) = 0``, so all scores are 0 — the instructive
    degenerate case. In the app, sentences act as documents. Ties are broken
    alphabetically for deterministic output.
    """
    n_docs = len(documents)
    if n_docs == 0:
        return []
    term_frequency: Counter[str] = Counter()
    document_frequency: Counter[str] = Counter()
    for document in documents:
        term_frequency.update(document)
        document_frequency.update(set(document))
    scored = [
        (term, round(count * log10(n_docs / document_frequency[term]), 4))
        for term, count in term_frequency.items()
    ]
    scored.sort(key=lambda item: (-item[1], item[0]))
    return [{"term": term, "score": score} for term, score in scored[:top_k]]


def kwic(
    tokens: list[str], keyword: str, window: int = 5, max_matches: int = 50
) -> list[dict[str, str]]:
    """Keyword-in-context concordance: every match with ``window`` tokens around it.

    Matching is case-insensitive on whole tokens. Returns at most
    ``max_matches`` rows of ``{"left", "keyword", "right"}`` with the context
    joined by single spaces.
    """
    target = keyword.lower()
    matches = []
    for index, token in enumerate(tokens):
        if token.lower() == target:
            matches.append(
                {
                    "left": " ".join(tokens[max(0, index - window) : index]),
                    "keyword": token,
                    "right": " ".join(tokens[index + 1 : index + 1 + window]),
                }
            )
            if len(matches) >= max_matches:
                break
    return matches


def zipf_table(tokens: list[str], top_k: int = 50) -> list[dict[str, str | int]]:
    """Rank-frequency table (Zipf's law view): rank 1 = most frequent token.

    Ties are broken alphabetically so ranks are deterministic. Plot
    ``log(rank)`` against ``log(count)``: natural text approximates a
    straight line of slope −1 (Zipf 1949).
    """
    counts = Counter(tokens)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:top_k]
    return [
        {"rank": rank, "term": term, "count": count}
        for rank, (term, count) in enumerate(ordered, start=1)
    ]


def vocabulary_growth(tokens: list[str], step: int = 100) -> list[dict[str, int]]:
    """Vocabulary size after every ``step`` tokens (type–token growth curve).

    Includes a final point at the full token count. Sub-linear growth is
    expected (Heaps' law); a flattening curve means fewer new word types per
    token read.
    """
    points = []
    seen: set[str] = set()
    for index, token in enumerate(tokens, start=1):
        seen.add(token)
        if index % step == 0:
            points.append({"tokens_seen": index, "vocabulary_size": len(seen)})
    if tokens and (not points or points[-1]["tokens_seen"] != len(tokens)):
        points.append({"tokens_seen": len(tokens), "vocabulary_size": len(seen)})
    return points


def _estimate_syllables(word: str, language: str = "English") -> int:
    """Estimate syllables by counting vowel groups (accented vowels included).

    The silent final ``e`` adjustment applies to English only. This is a
    heuristic: expect off-by-one errors on diphthongs, hiatus, and loanwords.
    Minimum result is 1.
    """
    word = word.lower()
    count = 0
    prev_is_vowel = False
    for char in word:
        is_vowel = char in _VOWELS
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    if language == "English" and word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)
