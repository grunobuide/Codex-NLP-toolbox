import unittest

from nlp_toolbox.languages import LANGUAGE_HINTS, STOPWORDS, get_language_config


class TestLanguages(unittest.TestCase):
    def test_get_language_config_known_language(self):
        config = get_language_config("English")
        self.assertEqual(config["name"], "English")
        self.assertEqual(config["stopwords"], STOPWORDS["English"])
        self.assertEqual(config["hints"], LANGUAGE_HINTS["English"])

    def test_get_language_config_unknown_language(self):
        config = get_language_config("Klingon")
        self.assertEqual(config["name"], "Klingon")
        self.assertEqual(config["stopwords"], set())
        self.assertEqual(config["hints"], set())


if __name__ == "__main__":
    unittest.main()
