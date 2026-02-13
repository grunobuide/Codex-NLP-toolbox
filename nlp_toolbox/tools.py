import re
from collections import Counter
from typing import Dict, List

from nlp_toolbox.languages import LANGUAGE_OPTIONS, get_language_config

WORD_PATTERN = re.compile(r"[\w']+", re.UNICODE)
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")
POSITIVE_WORDS = {
    "good",
    "great",
    "excellent",
    "positive",
    "fortunate",
    "correct",
    "superior",
    "happy",
    "love",
    "like",
    "joy",
    "delight",
    "amazing",
    "wonderful",
    "bright",
}
NEGATIVE_WORDS = {
    "bad",
    "terrible",
    "poor",
    "negative",
    "unfortunate",
    "wrong",
    "inferior",
    "sad",
    "hate",
    "dislike",
    "anger",
    "awful",
    "horrible",
    "dark",
}


def analyze_text(text: str, tokens: List[str], sentences: List[str]) -> dict:
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


def split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    sentences = SENTENCE_PATTERN.split(text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def tokenize_text(text: str, config: dict, lowercase: bool = True) -> List[str]:
    tokens = [match.group(0) for match in WORD_PATTERN.finditer(text)]
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens


def filter_tokens(
    tokens: List[str], config: dict, remove_stopwords: bool = True, min_length: int = 1
) -> List[str]:
    stopwords = config.get("stopwords", set()) if remove_stopwords else set()
    return [token for token in tokens if token not in stopwords and len(token) >= min_length]


def generate_ngrams(tokens: List[str], n: int) -> List[str]:
    if n <= 1:
        return tokens
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def extract_keywords(tokens: List[str], config: dict, top_k: int = 10) -> List[dict]:
    filtered = filter_tokens(tokens, config, remove_stopwords=True, min_length=1)
    frequencies = Counter(filtered).most_common(top_k)
    return [{"term": term, "count": count} for term, count in frequencies]


def top_ngrams(tokens: List[str], n: int, top_k: int = 10) -> List[dict]:
    ngrams = generate_ngrams(tokens, n)
    frequencies = Counter(ngrams).most_common(top_k)
    return [{"ngram": term, "count": count} for term, count in frequencies]


def readability_score(text: str, tokens: List[str], sentences: List[str]) -> float:
    if not tokens or not sentences:
        return 0.0
    syllables = sum(_estimate_syllables(token) for token in tokens)
    words_per_sentence = len(tokens) / max(len(sentences), 1)
    syllables_per_word = syllables / max(len(tokens), 1)
    score = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
    return round(score, 2)


def sentiment_analysis(tokens: List[str]) -> Dict[str, float]:
    positive = sum(1 for token in tokens if token in POSITIVE_WORDS)
    negative = sum(1 for token in tokens if token in NEGATIVE_WORDS)
    total = max(len(tokens), 1)
    score = round((positive - negative) / total, 3)
    return {
        "positive": positive,
        "negative": negative,
        "score": score,
    }


def word_length_distribution(tokens: List[str]) -> Dict[int, int]:
    lengths = Counter(len(token) for token in tokens)
    return dict(sorted(lengths.items(), key=lambda item: item[0]))


def language_hint_hits(tokens: List[str]) -> Dict[str, int]:
    scores = {}
    for language in LANGUAGE_OPTIONS:
        config = get_language_config(language)
        hints = config.get("hints", set())
        scores[language] = sum(1 for token in tokens if token in hints)
    return scores


def detect_language(text: str) -> str:
    tokens = tokenize_text(text, get_language_config("English"))
    if not tokens:
        return "English"

    scores = language_hint_hits(tokens)

    best_language = max(scores, key=scores.get)
    if scores[best_language] == 0:
        return "English"
    return best_language


def _estimate_syllables(word: str) -> int:
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev_is_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)
