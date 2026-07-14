import unittest

from nlp_toolbox.languages import get_language_config
from nlp_toolbox.tools import (
    _estimate_syllables,
    analyze_text,
    detect_language,
    detect_language_details,
    extract_keywords,
    filter_tokens,
    generate_ngrams,
    kwic,
    language_hint_hits,
    readability_score,
    sentiment_analysis,
    split_sentences,
    tfidf_keywords,
    tokenize_text,
    top_ngrams,
    vocabulary_growth,
    word_length_distribution,
    zipf_table,
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
        self.assertEqual(tokenize_text(text), ["hello", "nlp"])
        self.assertEqual(tokenize_text(text, lowercase=False), ["Hello", "NLP"])

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


class TestReadabilityFormulas(unittest.TestCase):
    """Pin the language-specific coefficients (regression guard)."""

    def setUp(self):
        # 1 sentence, 2 words, 5 syllables total: casa=2, bonita=3
        self.text = "Casa bonita."
        self.tokens = ["casa", "bonita"]
        self.sentences = ["Casa bonita."]
        self.wps = 2.0
        self.spw = 2.5

    def check(self, language, base, wps_c, spw_c):
        expected = round(base - wps_c * self.wps - spw_c * self.spw, 2)
        got = readability_score(self.text, self.tokens, self.sentences, language)
        self.assertAlmostEqual(got, expected, places=2)

    def test_spanish_fernandez_huerta(self):
        self.check("Spanish", 206.84, 1.02, 60.0)

    def test_french_kandel_moles(self):
        self.check("French", 207.0, 1.015, 73.6)

    def test_german_amstad(self):
        self.check("German", 180.0, 1.0, 58.5)

    def test_italian_franchina_vacca(self):
        self.check("Italian", 217.0, 1.3, 60.0)

    def test_portuguese_martins(self):
        self.check("Portuguese", 248.835, 1.015, 84.6)

    def test_unknown_language_falls_back_to_flesch(self):
        flesch = readability_score(self.text, self.tokens, self.sentences, "English")
        fallback = readability_score(self.text, self.tokens, self.sentences, "Klingon")
        self.assertEqual(fallback, flesch)

    def test_accented_vowels_counted(self):
        self.assertEqual(_estimate_syllables("café", "French"), 2)
        self.assertEqual(_estimate_syllables("perché", "Italian"), 2)
        self.assertEqual(_estimate_syllables("não", "Portuguese"), 1)
        self.assertEqual(_estimate_syllables("über", "German"), 2)

    def test_silent_e_only_in_english(self):
        self.assertEqual(_estimate_syllables("cake", "English"), 1)
        self.assertEqual(_estimate_syllables("cake", "German"), 2)


class TestTrack2Methods(unittest.TestCase):
    """Hand-computable examples for TF-IDF, KWIC, Zipf, and vocabulary growth."""

    def test_tfidf_hand_example(self):
        # tf: cat=2, sat=1, mat=1; df: cat=2, sat=1, mat=1; N=2
        # idf(cat)=log10(1)=0; idf(sat)=idf(mat)=log10(2)=0.30103
        result = tfidf_keywords([["cat", "sat"], ["cat", "mat"]])
        self.assertEqual(
            result,
            [
                {"term": "mat", "score": 0.301},
                {"term": "sat", "score": 0.301},
                {"term": "cat", "score": 0.0},
            ],
        )

    def test_tfidf_single_document_all_zero(self):
        result = tfidf_keywords([["cat", "sat", "cat"]])
        self.assertTrue(all(row["score"] == 0.0 for row in result))

    def test_tfidf_empty(self):
        self.assertEqual(tfidf_keywords([]), [])

    def test_kwic_window_and_case(self):
        tokens = ["a", "b", "KEY", "c", "d", "key"]
        result = kwic(tokens, "key", window=1)
        self.assertEqual(
            result,
            [
                {"left": "b", "keyword": "KEY", "right": "c"},
                {"left": "d", "keyword": "key", "right": ""},
            ],
        )

    def test_kwic_max_matches(self):
        tokens = ["key"] * 5
        self.assertEqual(len(kwic(tokens, "key", max_matches=3)), 3)

    def test_zipf_table_ranks_and_ties(self):
        result = zipf_table(["b", "a", "a", "c"], top_k=3)
        self.assertEqual(result[0], {"rank": 1, "term": "a", "count": 2})
        # tie between b and c broken alphabetically
        self.assertEqual(result[1], {"rank": 2, "term": "b", "count": 1})
        self.assertEqual(result[2], {"rank": 3, "term": "c", "count": 1})

    def test_vocabulary_growth_points(self):
        result = vocabulary_growth(["a", "b", "a", "c"], step=2)
        self.assertEqual(
            result,
            [
                {"tokens_seen": 2, "vocabulary_size": 2},
                {"tokens_seen": 4, "vocabulary_size": 3},
            ],
        )

    def test_vocabulary_growth_empty(self):
        self.assertEqual(vocabulary_growth([], step=2), [])


class TestDetectLanguageDetails(unittest.TestCase):
    def test_evidence_and_no_fallback(self):
        details = detect_language_details("el la que y de para")
        self.assertEqual(details.language, "Spanish")
        self.assertFalse(details.fallback)
        self.assertGreater(details.scores["Spanish"], 0)

    def test_zero_evidence_falls_back_to_english(self):
        details = detect_language_details("12345 xyzzy")
        self.assertEqual(details.language, "English")
        self.assertTrue(details.fallback)

    def test_tie_is_reported(self):
        # "que de" scores 2 for Spanish, French and Portuguese alike
        details = detect_language_details("que de")
        self.assertEqual(details.scores["Spanish"], details.scores["Portuguese"])
        self.assertIn("Portuguese", details.tied_with)
        self.assertFalse(details.fallback)


class TestMultilingualSentiment(unittest.TestCase):
    def test_portuguese(self):
        result = sentiment_analysis(["dia", "maravilhoso", "feliz"], "Portuguese")
        self.assertEqual(result["positive"], 2)
        self.assertEqual(result["negative"], 0)

    def test_spanish_negative(self):
        result = sentiment_analysis(["una", "película", "horrible"], "Spanish")
        self.assertEqual(result["negative"], 1)

    def test_no_negation_handling_documented_behavior(self):
        # "not good" counts the "good": known, documented limitation
        result = sentiment_analysis(["not", "good"])
        self.assertEqual(result["positive"], 1)

    def test_unsupported_language_scores_zero(self):
        result = sentiment_analysis(["good", "bad"], "Klingon")
        self.assertEqual(result, {"positive": 0, "negative": 0, "score": 0.0})


if __name__ == "__main__":
    unittest.main()
