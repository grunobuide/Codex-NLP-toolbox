"""Core NLP baselines: counting, regex, and lexicon methods.

Every function is a transparent baseline — its output can be reproduced by
hand. See ``docs/handbook/`` (planned) for worked examples and
``docs/resources.md`` for lexicon provenance.
"""

import re
from collections import Counter
from math import log, log10
from typing import NamedTuple

from nlp_toolbox.languages import (
    LANGUAGE_OPTIONS,
    LanguageConfig,
    get_language_config,
    load_ngram_profile,
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

    Includes a final point at the full token count. ``step`` must be >= 1
    (raises ``ValueError`` otherwise). Sub-linear growth is
    expected (Heaps' law); a flattening curve means fewer new word types per
    token read.
    """
    if step < 1:
        raise ValueError("step must be >= 1")
    points = []
    seen: set[str] = set()
    for index, token in enumerate(tokens, start=1):
        seen.add(token)
        if index % step == 0:
            points.append({"tokens_seen": index, "vocabulary_size": len(seen)})
    if tokens and (not points or points[-1]["tokens_seen"] != len(tokens)):
        points.append({"tokens_seen": len(tokens), "vocabulary_size": len(seen)})
    return points


def collocations(
    tokens: list[str], min_count: int = 3, top_k: int = 20
) -> list[dict[str, str | int | float]]:
    """Rank adjacent bigrams by log-likelihood ratio (Dunning 1993), with PMI.

    PMI = log2( p(xy) / (p(x) * p(y)) ) rewards pairs that co-occur more than
    chance predicts, but explodes for rare pairs — hence the ``min_count``
    floor and the LLR ranking. LLR (G²) compares the observed contingency
    table of the bigram against independence; it is robust at low counts.
    Reference: Dunning, T. (1993). Accurate methods for the statistics of
    surprise and coincidence. Computational Linguistics, 19(1).
    """
    n_bigrams = len(tokens) - 1
    if n_bigrams < 1:
        return []
    unigram_counts = Counter(tokens)
    bigram_counts = Counter(zip(tokens, tokens[1:], strict=False))

    def _entropy_term(k: int, n: int) -> float:
        return k * log(k / n) if k > 0 and n > 0 else 0.0

    results: list[dict[str, str | int | float]] = []
    for (first, second), count in bigram_counts.items():
        if count < min_count:
            continue
        c1 = sum(v for (a, _), v in bigram_counts.items() if a == first)
        c2 = sum(v for (_, b), v in bigram_counts.items() if b == second)
        # observed contingency table for the bigram
        k11 = count
        k12 = c1 - count
        k21 = c2 - count
        k22 = n_bigrams - c1 - c2 + count
        row1, row2 = k11 + k12, k21 + k22
        col1, col2 = k11 + k21, k12 + k22
        observed = sum(_entropy_term(k, n_bigrams) for k in (k11, k12, k21, k22))
        expected = (
            _entropy_term(row1, n_bigrams)
            + _entropy_term(row2, n_bigrams)
            + _entropy_term(col1, n_bigrams)
            + _entropy_term(col2, n_bigrams)
        ) - _entropy_term(n_bigrams, n_bigrams)
        llr = round(2 * (observed - expected), 4)
        p_xy = count / n_bigrams
        p_x = unigram_counts[first] / len(tokens)
        p_y = unigram_counts[second] / len(tokens)
        pmi = round(log(p_xy / (p_x * p_y), 2), 4)
        results.append({"bigram": f"{first} {second}", "count": count, "pmi": pmi, "llr": llr})
    results.sort(key=lambda row: (-float(row["llr"]), str(row["bigram"])))
    return results[:top_k]


_PORTER_VOWELS = "aeiou"


def porter_stem(word: str) -> str:
    """Porter stemmer (Porter 1980), the classic rule-based normalizer.

    A worked example of suffix-stripping morphology: transparent,
    language-specific (English only) and famously imperfect —
    ``university`` → ``univers``, ``relational`` → ``relat``. Failure cases
    are part of the lesson; see docs/error-analysis.md.
    Reference: Porter, M.F. (1980). An algorithm for suffix stripping.
    Program, 14(3).
    """
    word = word.lower()
    if len(word) <= 2:
        return word

    def is_consonant(w: str, i: int) -> bool:
        char = w[i]
        if char in _PORTER_VOWELS:
            return False
        if char == "y":
            return i == 0 or not is_consonant(w, i - 1)
        return True

    def measure(stem: str) -> int:
        forms = "".join("c" if is_consonant(stem, i) else "v" for i in range(len(stem)))
        return forms.count("vc")

    def has_vowel(stem: str) -> bool:
        return any(not is_consonant(stem, i) for i in range(len(stem)))

    def ends_double_consonant(stem: str) -> bool:
        return len(stem) >= 2 and stem[-1] == stem[-2] and is_consonant(stem, len(stem) - 1)

    def ends_cvc(stem: str) -> bool:
        if len(stem) < 3:
            return False
        return (
            is_consonant(stem, len(stem) - 3)
            and not is_consonant(stem, len(stem) - 2)
            and is_consonant(stem, len(stem) - 1)
            and stem[-1] not in "wxy"
        )

    # step 1a
    if word.endswith("sses") or word.endswith("ies"):
        word = word[:-2]
    elif not word.endswith("ss") and word.endswith("s"):
        word = word[:-1]

    # step 1b
    if word.endswith("eed"):
        if measure(word[:-3]) > 0:
            word = word[:-1]
    else:
        flag = False
        if word.endswith("ed") and has_vowel(word[:-2]):
            word, flag = word[:-2], True
        elif word.endswith("ing") and has_vowel(word[:-3]):
            word, flag = word[:-3], True
        if flag:
            if word.endswith(("at", "bl", "iz")):
                word += "e"
            elif ends_double_consonant(word) and word[-1] not in "lsz":
                word = word[:-1]
            elif measure(word) == 1 and ends_cvc(word):
                word += "e"

    # step 1c
    if word.endswith("y") and has_vowel(word[:-1]):
        word = word[:-1] + "i"

    def replace(end: str, repl: str, min_measure: int = 0) -> bool:
        nonlocal word
        if word.endswith(end) and measure(word[: -len(end)]) > min_measure:
            word = word[: -len(end)] + repl
            return True
        return word.endswith(end)

    # step 2
    for end, repl in (
        ("ational", "ate"),
        ("tional", "tion"),
        ("enci", "ence"),
        ("anci", "ance"),
        ("izer", "ize"),
        ("abli", "able"),
        ("alli", "al"),
        ("entli", "ent"),
        ("eli", "e"),
        ("ousli", "ous"),
        ("ization", "ize"),
        ("ation", "ate"),
        ("ator", "ate"),
        ("alism", "al"),
        ("iveness", "ive"),
        ("fulness", "ful"),
        ("ousness", "ous"),
        ("aliti", "al"),
        ("iviti", "ive"),
        ("biliti", "ble"),
    ):
        if word.endswith(end):
            replace(end, repl)
            break

    # step 3
    for end, repl in (
        ("icate", "ic"),
        ("ative", ""),
        ("alize", "al"),
        ("iciti", "ic"),
        ("ical", "ic"),
        ("ful", ""),
        ("ness", ""),
    ):
        if word.endswith(end):
            replace(end, repl)
            break

    # step 4
    for end in (
        "al",
        "ance",
        "ence",
        "er",
        "ic",
        "able",
        "ible",
        "ant",
        "ement",
        "ment",
        "ent",
        "ou",
        "ism",
        "ate",
        "iti",
        "ous",
        "ive",
        "ize",
    ):
        if word.endswith(end):
            if measure(word[: -len(end)]) > 1:
                word = word[: -len(end)]
            break
    else:
        if word.endswith("ion") and len(word) > 3 and word[-4] in "st" and measure(word[:-3]) > 1:
            word = word[:-3]

    # step 5a
    if word.endswith("e"):
        stem = word[:-1]
        if measure(stem) > 1 or (measure(stem) == 1 and not ends_cvc(stem)):
            word = stem

    # step 5b
    if measure(word) > 1 and ends_double_consonant(word) and word.endswith("l"):
        word = word[:-1]

    return word


def build_ngram_profile(text: str, size: int = 300) -> list[str]:
    """Ranked character-trigram profile of ``text`` (Cavnar-Trenkle 1994).

    Normalization: lowercase; every non-letter run becomes a single ``_``
    (word boundary); trigrams containing at least one letter are counted
    and ranked by frequency (ties alphabetical). Reference: Cavnar, W. &
    Trenkle, J. (1994). N-gram-based text categorization. SDAIR-94.
    """
    normalized = "".join(ch if ch.isalpha() else "_" for ch in text.lower())
    normalized = "_" + re.sub(r"_+", "_", normalized) + "_"
    counts = Counter(
        normalized[i : i + 3]
        for i in range(len(normalized) - 2)
        if any(ch.isalpha() for ch in normalized[i : i + 3])
    )
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [trigram for trigram, _ in ranked[:size]]


class NgramDetection(NamedTuple):
    """Outcome of character n-gram language detection.

    ``distances`` maps each language to its out-of-place distance from the
    text profile — LOWER is closer. ``fallback`` is True when the text has
    no letters (English by convention, same contract as the hint-word
    detector).
    """

    language: str
    distances: dict[str, int]
    fallback: bool


def detect_language_ngram_details(text: str) -> NgramDetection:
    """Detect language by comparing trigram profiles (out-of-place distance).

    For each trigram in the text profile, the penalty is the absolute
    difference between its rank in the text and its rank in the language
    profile (missing: penalty = profile size). Fully inspectable: every
    penalty can be recomputed from the shipped profile files.
    """
    text_profile = build_ngram_profile(text)
    if not text_profile:
        return NgramDetection("English", {}, True)
    distances: dict[str, int] = {}
    for language in LANGUAGE_OPTIONS:
        profile = load_ngram_profile(language)
        ranks = {trigram: rank for rank, trigram in enumerate(profile)}
        max_penalty = len(profile)
        distances[language] = sum(
            abs(rank - ranks[trigram]) if trigram in ranks else max_penalty
            for rank, trigram in enumerate(text_profile)
        )
    best = min(LANGUAGE_OPTIONS, key=lambda lang: distances[lang])
    return NgramDetection(best, distances, False)


def detect_language_ngram(text: str) -> str:
    """Convenience wrapper over ``detect_language_ngram_details``."""
    return detect_language_ngram_details(text).language


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
