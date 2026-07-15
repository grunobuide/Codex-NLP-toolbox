"""Key-parity tests for the bilingual didactic layer (``app_i18n``).

These guard against the classic i18n bug: a string added to one language and
forgotten in the other. They assert English and Portuguese expose exactly the
same keys everywhere, and that every method card is complete in both languages.
"""

import unittest

import app_i18n


class TestI18nParity(unittest.TestCase):
    def test_languages_map(self):
        self.assertEqual(set(app_i18n.LANGUAGES.values()), {"en", "pt"})

    def test_ui_key_parity(self):
        self.assertEqual(set(app_i18n.UI["en"]), set(app_i18n.UI["pt"]))

    def test_ui_values_nonempty(self):
        for lang in ("en", "pt"):
            for key, value in app_i18n.UI[lang].items():
                self.assertTrue(value.strip(), f"empty UI string {lang}/{key}")

    def test_theme_labels_cover_order(self):
        for lang in ("en", "pt"):
            self.assertEqual(set(app_i18n.THEME_LABELS[lang]), set(app_i18n.THEME_ORDER))

    def test_card_labels_parity(self):
        self.assertEqual(set(app_i18n.CARD_LABELS["en"]), set(app_i18n.CARD_LABELS["pt"]))

    def test_every_card_complete_in_both_languages(self):
        fields = {"what", "how", "why", "explore"}
        for tool, card in app_i18n.TOOL_CARDS.items():
            self.assertIn(card["theme"], app_i18n.THEME_ORDER, f"{tool} has unknown theme")
            for lang in ("en", "pt"):
                self.assertIn(lang, card, f"{tool} missing {lang}")
                self.assertEqual(set(card[lang]), fields, f"{tool}/{lang} field mismatch")
                for field, text in card[lang].items():
                    self.assertTrue(text.strip(), f"empty {tool}/{lang}/{field}")

    def test_ui_format_placeholders_match(self):
        import re

        def placeholders(text: str) -> set[str]:
            return set(re.findall(r"\{(\w+)\}", text))

        for key in app_i18n.UI["en"]:
            self.assertEqual(
                placeholders(app_i18n.UI["en"][key]),
                placeholders(app_i18n.UI["pt"][key]),
                f"format-placeholder mismatch in UI key {key!r}",
            )


if __name__ == "__main__":
    unittest.main()
