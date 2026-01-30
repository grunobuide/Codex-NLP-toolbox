import re
from collections import Counter
from typing import List

from nlp_toolbox.languages import LANGUAGE_OPTIONS, get_language_config

WORD_PATTERN = re.compile(r"[\w']+", re.UNICODE)
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")


def analyze_text(text: str) -> dict:
    tokens = tokenize_text(text, get_language_config("English"))
    sentences = split_sentences(text)
    return {
        "characters": len(text),
        "words": len(tokens),
        "sentences": len(sentences),
        "avg_word_length": round(sum(len(token) for token in tokens) / max(len(tokens), 1), 2),
    }


def split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    sentences = SENTENCE_PATTERN.split(text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def tokenize_text(text: str, config: dict) -> List[str]:
    tokens = [match.group(0).lower() for match in WORD_PATTERN.finditer(text)]
    return tokens


def generate_ngrams(tokens: List[str], n: int) -> List[str]:
    if n <= 1:
        return tokens
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def extract_keywords(tokens: List[str], config: dict, top_k: int = 10) -> List[dict]:
    stopwords = config.get("stopwords", set())
    filtered = [token for token in tokens if token not in stopwords]
    frequencies = Counter(filtered).most_common(top_k)
    return [{"term": term, "count": count} for term, count in frequencies]


def detect_language(text: str) -> str:
    tokens = tokenize_text(text, get_language_config("English"))
    if not tokens:
        return "English"

    scores = {}
    for language in LANGUAGE_OPTIONS:
        config = get_language_config(language)
        hints = config.get("hints", set())
        scores[language] = sum(1 for token in tokens if token in hints)

    best_language = max(scores, key=scores.get)
    if scores[best_language] == 0:
        return "English"
    return best_language
