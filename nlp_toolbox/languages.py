"""Language configuration: supported languages, stopwords, and detection hints.

Stopword lists are adapted from spaCy 3.8 (MIT license); see ``docs/resources.md``
for provenance, sizes, and known limitations of each list.
"""

from functools import cache
from importlib import resources
from typing import TypedDict


class LanguageConfig(TypedDict):
    """Bundle of language-specific resources used across the toolbox."""

    name: str
    stopwords: set[str]
    hints: set[str]


LANGUAGE_OPTIONS = ["English", "Spanish", "French", "German", "Italian", "Portuguese"]

_LANGUAGE_CODES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
}

# Small, high-frequency function words used by the transparent hint-word
# language detector (see ``tools.detect_language``). Deliberately tiny so the
# evidence table stays human-readable; a character n-gram detector is planned
# as a stronger interpretable alternative (CONTENT_ROADMAP Track 1).
LANGUAGE_HINTS = {
    "English": {"the", "and", "is", "of", "to", "with", "that"},
    "Spanish": {"el", "la", "que", "y", "de", "para"},
    "French": {"le", "la", "que", "et", "de", "pour"},
    "German": {"der", "die", "und", "zu", "mit", "ist"},
    "Italian": {"il", "la", "che", "e", "di", "per"},
    "Portuguese": {"o", "a", "que", "e", "de", "para"},
}


@cache
def load_stopwords(language_name: str) -> frozenset[str]:
    """Load the stopword list for ``language_name`` from packaged resources.

    Returns an empty set for unsupported languages rather than raising, so
    callers can treat "no stopwords available" as a degraded-but-valid state.
    """
    code = _LANGUAGE_CODES.get(language_name)
    if code is None:
        return frozenset()
    ref = resources.files("nlp_toolbox.resources.stopwords").joinpath(f"{code}.txt")
    text = ref.read_text(encoding="utf-8")
    return frozenset(line.strip() for line in text.splitlines() if line.strip())


@cache
def load_sentiment_lexicon(language_name: str) -> tuple[frozenset[str], frozenset[str]]:
    """Load (positive, negative) word sets for ``language_name``.

    Hand-curated v1 lexicons (~75-100 words per polarity per language);
    methodology and limitations in ``docs/resources.md``. Unsupported
    languages get empty sets, so sentiment scores degrade to 0 rather
    than failing.
    """
    code = _LANGUAGE_CODES.get(language_name)
    if code is None:
        return frozenset(), frozenset()
    base = resources.files("nlp_toolbox.resources.sentiment")

    def _read(polarity: str) -> frozenset[str]:
        text = base.joinpath(f"{code}_{polarity}.txt").read_text(encoding="utf-8")
        return frozenset(line.strip() for line in text.splitlines() if line.strip())

    return _read("positive"), _read("negative")


def get_language_config(language_name: str) -> LanguageConfig:
    """Return the stopwords and detection hints for ``language_name``.

    Unsupported names yield a config with empty word sets (never ``None``),
    keeping downstream tools total functions over their inputs.
    """
    return {
        "name": language_name,
        "stopwords": set(load_stopwords(language_name)),
        "hints": set(LANGUAGE_HINTS.get(language_name, set())),
    }
