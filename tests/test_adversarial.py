"""Adversarial and ambiguous inputs as regression fixtures.

Each test pins today's *observed* behavior — including behavior that is
wrong-but-documented. If an improvement changes one of these outcomes,
the test failure is the changelog entry. Root causes: docs/error-analysis.md.
"""

import unittest

from nlp_toolbox.tools import (
    detect_language_details,
    sentiment_analysis,
    split_sentences,
    tokenize_text,
)


class TestLanguageDetectionAdversarial(unittest.TestCase):
    def test_code_switching_picks_one_language(self):
        # PT/EN code-switching: detector must pick one, with visible evidence
        details = detect_language_details(
            "O deploy falhou but the rollback worked e o time ficou feliz."
        )
        self.assertIn(details.language, {"Portuguese", "English"})
        self.assertGreater(details.scores["Portuguese"], 0)
        self.assertGreater(details.scores["English"], 0)

    def test_digits_only_falls_back(self):
        details = detect_language_details("123 456 789")
        self.assertTrue(details.fallback)
        self.assertEqual(details.language, "English")

    def test_emoji_only_falls_back(self):
        details = detect_language_details("🎉🎊✨")
        self.assertTrue(details.fallback)

    def test_non_latin_script_falls_back_to_english(self):
        # Known limitation: Cyrillic/CJK text gets 'English' with fallback flag —
        # the hint lexicons only cover six Latin-script languages.
        for text in ["Это русский текст без подсказок", "これは日本語の文章です"]:
            details = detect_language_details(text)
            self.assertTrue(details.fallback, text)

    def test_spanish_portuguese_confusion_short_text(self):
        # 'de' and 'que' are hint words for ES, FR and PT simultaneously:
        # short Romance texts tie and resolve by fixed order (Spanish first).
        details = detect_language_details("que de")
        self.assertEqual(details.language, "Spanish")
        self.assertIn("Portuguese", details.tied_with)


class TestSentimentAdversarial(unittest.TestCase):
    def test_negation_inverts_nothing(self):
        # Documented failure: negation is invisible to the lexicon.
        self.assertGreater(sentiment_analysis(tokenize_text("this is not good at all"))["score"], 0)

    def test_zero_evidence_scores_zero(self):
        result = sentiment_analysis(tokenize_text("The quarterly report was submitted on Tuesday."))
        self.assertEqual((result["positive"], result["negative"]), (0, 0))

    def test_uppercase_input_without_lowercasing_misses_lexicon(self):
        # Contract: tokens must be lowercase. Raw uppercase tokens miss.
        self.assertEqual(sentiment_analysis(["GOOD", "BAD"])["score"], 0.0)


class TestSegmentationAdversarial(unittest.TestCase):
    def test_abbreviation_oversplits(self):
        # Documented failure: 'Dr. Smith' splits after 'Dr.'
        sentences = split_sentences("Dr. Smith arrived. He was late.")
        self.assertEqual(len(sentences), 3)

    def test_no_terminal_punctuation_undersplits(self):
        sentences = split_sentences("first line\nsecond line\nthird line")
        self.assertEqual(len(sentences), 1)

    def test_ellipsis_and_decimal_numbers(self):
        self.assertEqual(len(split_sentences("Wait... really? Yes.")), 3)
        # decimal point does not split (no following whitespace)
        self.assertEqual(len(split_sentences("Pi is 3.14 exactly.")), 1)


class TestTokenizerAdversarial(unittest.TestCase):
    def test_apostrophes_kept_hyphens_split(self):
        self.assertEqual(tokenize_text("don't"), ["don't"])
        self.assertEqual(tokenize_text("state-of-the-art"), ["state", "of", "the", "art"])

    def test_emoji_not_tokens_but_underscore_is(self):
        self.assertEqual(tokenize_text("great 🎉 day"), ["great", "day"])
        # \w includes underscore: snake_case survives as one token
        self.assertEqual(tokenize_text("snake_case"), ["snake_case"])

    def test_accented_and_non_latin_word_chars_kept(self):
        self.assertEqual(tokenize_text("café über ação"), ["café", "über", "ação"])
        self.assertEqual(tokenize_text("русский"), ["русский"])


if __name__ == "__main__":
    unittest.main()
