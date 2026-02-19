import unittest

from nlp_toolbox.languages import get_language_config
from nlp_toolbox.tools import (
    _estimate_syllables,
    analyze_text,
    detect_language,
    extract_keywords,
    filter_tokens,
    generate_ngrams,
    language_hint_hits,
    readability_score,
    sentiment_analysis,
    split_sentences,
    tokenize_text,
    top_ngrams,
    word_length_distribution,
)


class TestNlpTools(unittest.TestCase):
    def setUp(self):
        self.english = get_language_config("English")

    def test_split_sentences(self):
        text = "Hello world. How are you? I'm fine!"
        self.assertEqual(split_sentences(text), ["Hello world.", "How are you?", "I'm fine!"])
        self.assertEqual(split_sentences("   "), [])

    def test_tokenize_text_lowercase_toggle(self):
        text = "Hello NLP"
        self.assertEqual(tokenize_text(text, self.english), ["hello", "nlp"])
        self.assertEqual(tokenize_text(text, self.english, lowercase=False), ["Hello", "NLP"])

    def test_filter_tokens(self):
        tokens = ["the", "quick", "fox", "jumps"]
        self.assertEqual(
            filter_tokens(tokens, self.english, remove_stopwords=True, min_length=4),
            ["quick", "jumps"],
        )
        self.assertEqual(
            filter_tokens(tokens, self.english, remove_stopwords=False, min_length=1),
            tokens,
        )

    def test_generate_ngrams(self):
        tokens = ["a", "b", "c"]
        self.assertEqual(generate_ngrams(tokens, 2), ["a b", "b c"])
        self.assertEqual(generate_ngrams(tokens, 1), tokens)

    def test_extract_keywords(self):
        tokens = ["the", "cat", "cat", "sat"]
        self.assertEqual(
            extract_keywords(tokens, self.english, top_k=2),
            [{"term": "cat", "count": 2}, {"term": "sat", "count": 1}],
        )

    def test_top_ngrams(self):
        tokens = ["nlp", "is", "fun", "nlp", "is", "fun"]
        self.assertEqual(top_ngrams(tokens, 2, top_k=1), [{"ngram": "nlp is", "count": 2}])

    def test_analyze_text(self):
        text = "Hello world."
        tokens = ["hello", "world"]
        sentences = ["Hello world."]
        stats = analyze_text(text, tokens, sentences)
        self.assertEqual(stats["characters"], len(text))
        self.assertEqual(stats["words"], 2)
        self.assertEqual(stats["sentences"], 1)
        self.assertEqual(stats["unique_words"], 2)

    def test_readability_score(self):
        text = "Simple sentence."
        tokens = ["simple", "sentence"]
        sentences = ["Simple sentence."]
        self.assertIsInstance(readability_score(text, tokens, sentences), float)
        self.assertEqual(readability_score("", [], []), 0.0)

    def test_sentiment_analysis(self):
        tokens = ["good", "amazing", "bad"]
        result = sentiment_analysis(tokens)
        self.assertEqual(result["positive"], 2)
        self.assertEqual(result["negative"], 1)
        self.assertEqual(result["score"], 0.333)

    def test_word_length_distribution(self):
        tokens = ["a", "to", "dog", "cat"]
        self.assertEqual(word_length_distribution(tokens), {1: 1, 2: 1, 3: 2})

    def test_language_hint_hits_and_detect_language(self):
        tokens = ["el", "la", "que", "y"]
        hints = language_hint_hits(tokens)
        self.assertGreater(hints["Spanish"], 0)

        detected = detect_language("el la que y")
        self.assertEqual(detected, "Spanish")
        self.assertEqual(detect_language("12345"), "English")

    def test_estimate_syllables(self):
        self.assertEqual(_estimate_syllables("cake"), 1)
        self.assertEqual(_estimate_syllables("banana"), 3)
        self.assertEqual(_estimate_syllables("rhythm"), 1)


if __name__ == "__main__":
    unittest.main()
