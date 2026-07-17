"""Pinned expected results for the course's lesson presets (Aula 4 pilot).

Every number quoted in a lesson script, preset or answer key must be
reproducible; these tests pin the exact outputs the course materials cite
(docs/course/aula-04/). If a change breaks one of these, either the change is
a bug or the lesson materials must be updated in the same commit — never let
the recorded numbers drift silently from the app.

The char n-gram expectations depend on the frozen profiles in
``nlp_toolbox/resources/ngram_profiles/``; regenerating profiles is a
deliberate versioned change that must update these pins too.
"""

import unittest

from nlp_toolbox.tools import (
    detect_language_details,
    detect_language_ngram_details,
    language_hint_evidence,
    tokenize_text,
)

FRASE_PT = (
    "O gato subiu no telhado e a casa ficou em silêncio, o que preocupou a vizinha de Capitu."
)
QUE_DE = "que de"
RUSSO = "Я не понимаю, что здесь написано, но всё равно интересно."
DUAS_PALAVRAS_PT = "telhado bonito"


class TestAula04Preset(unittest.TestCase):
    def test_frase_pt_hints_evidence(self):
        details = detect_language_details(FRASE_PT)
        self.assertEqual(details.language, "Portuguese")
        self.assertFalse(details.fallback)
        self.assertEqual(details.tied_with, [])
        self.assertEqual(
            details.scores,
            {
                "English": 0,
                "Spanish": 2,
                "French": 2,
                "German": 0,
                "Italian": 1,
                "Portuguese": 7,
            },
        )
        evidence = language_hint_evidence(tokenize_text(FRASE_PT))
        self.assertEqual(evidence["Portuguese"], {"o": 2, "a": 2, "e": 1, "que": 1, "de": 1})
        self.assertEqual(evidence["Spanish"], {"que": 1, "de": 1})
        self.assertEqual(evidence["French"], {"que": 1, "de": 1})
        self.assertEqual(evidence["English"], {})

    def test_frase_pt_ngram_agrees(self):
        details = detect_language_ngram_details(FRASE_PT)
        self.assertEqual(details.language, "Portuguese")
        ranked = sorted(details.distances, key=lambda lang: details.distances[lang])
        self.assertEqual(ranked[0], "Portuguese")
        self.assertEqual(ranked[1], "Spanish")

    def test_que_de_hints_tie_resolved_by_order(self):
        details = detect_language_details(QUE_DE)
        self.assertEqual(details.language, "Spanish")  # fixed-order bias, on purpose
        self.assertEqual(sorted(details.tied_with), ["French", "Portuguese"])
        self.assertEqual(details.scores["Spanish"], 2)
        self.assertEqual(details.scores["French"], 2)
        self.assertEqual(details.scores["Portuguese"], 2)

    def test_que_de_ngram_disagrees_with_hints(self):
        # The two transparent detectors legitimately disagree on this
        # ambiguous input - the lesson's key discussion moment.
        details = detect_language_ngram_details(QUE_DE)
        self.assertEqual(details.language, "French")
        self.assertEqual(details.distances["French"], 60)
        self.assertEqual(details.distances["Portuguese"], 133)
        self.assertEqual(details.distances["Spanish"], 180)

    def test_russo_hints_fallback(self):
        details = detect_language_details(RUSSO)
        self.assertEqual(details.language, "English")
        self.assertTrue(details.fallback)
        self.assertEqual(sum(details.scores.values()), 0)
        evidence = language_hint_evidence(tokenize_text(RUSSO))
        self.assertTrue(all(matched == {} for matched in evidence.values()))

    def test_russo_ngram_max_distance_tie(self):
        # Documented limitation: Cyrillic trigrams miss every Latin profile,
        # so all distances hit the same maximum and the tie is resolved by
        # fixed language order (English) - WITHOUT a fallback flag. The
        # lesson shows this as an honest gap of the current implementation.
        details = detect_language_ngram_details(RUSSO)
        self.assertEqual(details.language, "English")
        self.assertFalse(details.fallback)
        self.assertEqual(len(set(details.distances.values())), 1)

    def test_duas_palavras_short_text_contrast(self):
        # Hint words: zero evidence -> English fallback (the 28.9% regime).
        hints = detect_language_details(DUAS_PALAVRAS_PT)
        self.assertEqual(hints.language, "English")
        self.assertTrue(hints.fallback)
        # Char n-grams: correct on the same two words (the 61% regime).
        ngram = detect_language_ngram_details(DUAS_PALAVRAS_PT)
        self.assertEqual(ngram.language, "Portuguese")
        ranked = sorted(ngram.distances, key=lambda lang: ngram.distances[lang])
        self.assertEqual(ranked[0], "Portuguese")
        self.assertEqual(ranked[1], "Spanish")


if __name__ == "__main__":
    unittest.main()
