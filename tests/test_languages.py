import unittest

from nlp_toolbox.languages import (
    LANGUAGE_HINTS,
    LANGUAGE_OPTIONS,
    get_language_config,
    load_stopwords,
)


class TestLanguages(unittest.TestCase):
    def test_all_languages_have_real_stopword_lists(self):
        for language in LANGUAGE_OPTIONS:
            with self.subTest(language=language):
                stopwords = load_stopwords(language)
                self.assertGreater(len(stopwords), 100)

    def test_known_entries_present(self):
        self.assertIn("the", load_stopwords("English"))
        self.assertIn("para", load_stopwords("Portuguese"))
        self.assertIn("und", load_stopwords("German"))
        self.assertIn("perché", load_stopwords("Italian"))

    def test_stopwords_are_lowercase_and_stripped(self):
        for language in LANGUAGE_OPTIONS:
            for word in load_stopwords(language):
                self.assertEqual(word, word.strip())
                self.assertEqual(word, word.lower())

    def test_get_language_config_known_language(self):
        config = get_language_config("English")
        self.assertEqual(config["name"], "English")
        self.assertEqual(config["stopwords"], set(load_stopwords("English")))
        self.assertEqual(config["hints"], LANGUAGE_HINTS["English"])

    def test_get_language_config_unknown_language(self):
        config = get_language_config("Klingon")
        self.assertEqual(config["name"], "Klingon")
        self.assertEqual(config["stopwords"], set())
        self.assertEqual(config["hints"], set())

    def test_load_stopwords_is_cached(self):
        self.assertIs(load_stopwords("English"), load_stopwords("English"))


if __name__ == "__main__":
    unittest.main()
