"""Property-based tests: invariants that must hold for arbitrary input.

Born in the Phase 4 error analysis. Each property is a contract stated in
the docstrings of nlp_toolbox; Hypothesis tries to break it with arbitrary
Unicode. See docs/error-analysis.md for the failures these tests pinned.
"""

import unittest

from hypothesis import given, settings
from hypothesis import strategies as st

from nlp_toolbox.languages import LANGUAGE_OPTIONS, get_language_config
from nlp_toolbox.tools import (
    analyze_text,
    detect_language_details,
    filter_tokens,
    generate_ngrams,
    kwic,
    readability_score,
    sentiment_analysis,
    split_sentences,
    tfidf_keywords,
    tokenize_text,
    vocabulary_growth,
    word_length_distribution,
    zipf_table,
)

any_text = st.text(max_size=300)
tokens_list = st.lists(st.text(min_size=1, max_size=15), max_size=50)


class TestUniversalRobustness(unittest.TestCase):
    """No public function may crash on arbitrary Unicode text."""

    @given(any_text)
    @settings(max_examples=200)
    def test_full_pipeline_never_crashes(self, text):
        config = get_language_config("English")
        sentences = split_sentences(text)
        tokens = tokenize_text(text)
        filter_tokens(tokens, config)
        analyze_text(text, tokens, sentences)
        readability_score(text, tokens, sentences)
        sentiment_analysis(tokens)
        word_length_distribution(tokens)
        zipf_table(tokens)
        detect_language_details(text)

    @given(any_text)
    def test_detection_always_returns_supported_language(self, text):
        details = detect_language_details(text)
        self.assertIn(details.language, LANGUAGE_OPTIONS)
        if details.fallback:
            self.assertEqual(details.language, "English")
            self.assertEqual(max(details.scores.values(), default=0), 0)


class TestStructuralInvariants(unittest.TestCase):
    @given(tokens_list)
    def test_filter_tokens_is_subsequence(self, tokens):
        filtered = filter_tokens(tokens, get_language_config("English"))
        it = iter(tokens)
        self.assertTrue(all(any(t == u for u in it) for t in filtered))

    @given(tokens_list, st.integers(min_value=2, max_value=6))
    def test_ngram_count(self, tokens, n):
        ngrams = generate_ngrams(tokens, n)
        self.assertEqual(len(ngrams), max(len(tokens) - n + 1, 0))

    @given(tokens_list)
    def test_zipf_ranks_and_counts_monotone(self, tokens):
        table = zipf_table(tokens)
        ranks = [row["rank"] for row in table]
        counts = [row["count"] for row in table]
        self.assertEqual(ranks, list(range(1, len(table) + 1)))
        self.assertEqual(counts, sorted(counts, reverse=True))

    @given(tokens_list, st.integers(min_value=1, max_value=20))
    def test_vocabulary_growth_monotone_and_bounded(self, tokens, step):
        points = vocabulary_growth(tokens, step=step)
        sizes = [p["vocabulary_size"] for p in points]
        self.assertEqual(sizes, sorted(sizes))
        for point in points:
            self.assertLessEqual(point["vocabulary_size"], point["tokens_seen"])
        if tokens:
            self.assertEqual(points[-1]["tokens_seen"], len(tokens))

    def test_vocabulary_growth_rejects_bad_step(self):
        # regression: step=0 used to raise ZeroDivisionError (found in Phase 4)
        with self.assertRaises(ValueError):
            vocabulary_growth(["a"], step=0)

    @given(tokens_list)
    def test_sentiment_counts_bounded_by_tokens(self, tokens):
        for language in LANGUAGE_OPTIONS:
            result = sentiment_analysis(tokens, language)
            self.assertLessEqual(result["positive"] + result["negative"], len(tokens))
            self.assertGreaterEqual(result["score"], -1.0)
            self.assertLessEqual(result["score"], 1.0)

    @given(st.lists(st.lists(st.text(min_size=1, max_size=8), max_size=10), max_size=8))
    def test_tfidf_scores_non_negative(self, documents):
        for row in tfidf_keywords(documents):
            self.assertGreaterEqual(row["score"], 0.0)

    @given(tokens_list, st.text(min_size=1, max_size=10), st.integers(min_value=0, max_value=8))
    def test_kwic_matches_are_real_and_bounded(self, tokens, keyword, window):
        matches = kwic(tokens, keyword, window=window)
        self.assertLessEqual(len(matches), 50)
        for match in matches:
            self.assertEqual(match["keyword"].lower(), keyword.lower())

    @given(any_text)
    def test_split_sentences_returns_stripped_nonempty(self, text):
        for sentence in split_sentences(text):
            self.assertTrue(sentence)
            self.assertEqual(sentence, sentence.strip())


if __name__ == "__main__":
    unittest.main()
