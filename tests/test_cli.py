import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from nlp_toolbox.cli import main


def run_cli(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    with redirect_stdout(out):
        code = main(list(argv))
    return code, out.getvalue()


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file = Path(self.tmp.name) / "sample.txt"
        self.file.write_text(
            "O gato subiu no telhado. O gato dormiu. A casa é bonita e o telhado é velho.",
            encoding="utf-8",
        )

    def test_analyze_json(self):
        code, out = run_cli("analyze", str(self.file), "--json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["language"], "Portuguese")
        self.assertFalse(payload["language_detection_fallback"])
        self.assertEqual(payload["readability"]["formula"], "Flesch adaptado (Martins et al.)")
        self.assertGreater(payload["stats"]["words"], 10)

    def test_analyze_explicit_language(self):
        code, out = run_cli("analyze", str(self.file), "--lang", "English", "--json")
        payload = json.loads(out)
        self.assertEqual(payload["language"], "English")
        self.assertEqual(payload["readability"]["formula"], "Flesch Reading Ease")

    def test_keywords_freq_vs_tfidf(self):
        code, out = run_cli("keywords", str(self.file), "--method", "freq", "--json")
        freq = json.loads(out)
        self.assertEqual(freq["method"], "freq")
        self.assertTrue(any(row["term"] == "gato" for row in freq["keywords"]))

        code, out = run_cli("keywords", str(self.file), "--method", "tfidf", "--json")
        tfidf = json.loads(out)
        self.assertEqual(tfidf["method"], "tfidf")
        self.assertIn("score", tfidf["keywords"][0])

    def test_kwic(self):
        code, out = run_cli("kwic", str(self.file), "gato", "--window", "2", "--json")
        payload = json.loads(out)
        self.assertEqual(len(payload["matches"]), 2)
        self.assertEqual(payload["matches"][0]["keyword"], "gato")

    def test_zipf(self):
        code, out = run_cli("zipf", str(self.file), "--top-k", "3", "--json")
        payload = json.loads(out)
        self.assertEqual(len(payload["table"]), 3)
        self.assertEqual(payload["table"][0]["rank"], 1)

    def test_language_char_ngram_default(self):
        code, out = run_cli("language", str(self.file), "--json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["method"], "char-ngram")
        self.assertEqual(payload["language"], "Portuguese")
        self.assertIn("distances", payload)
        self.assertFalse(payload["fallback"])

    def test_language_hints_method(self):
        code, out = run_cli("language", str(self.file), "--method", "hints", "--json")
        payload = json.loads(out)
        self.assertEqual(payload["method"], "hints")
        self.assertEqual(payload["language"], "Portuguese")
        self.assertIn("scores", payload)

    def test_language_compare(self):
        code, out = run_cli("language", str(self.file), "--compare", "--json")
        payload = json.loads(out)
        self.assertIn("hints", payload)
        self.assertIn("char_ngram", payload)
        self.assertEqual(payload["hints"]["language"], "Portuguese")
        self.assertEqual(payload["char_ngram"]["language"], "Portuguese")
        self.assertTrue(payload["agree"])

    def test_missing_file_returns_2(self):
        err = io.StringIO()
        with redirect_stderr(err):
            code, _ = run_cli("analyze", "/no/such/file.txt", "--json")
        self.assertEqual(code, 2)
        self.assertIn("file not found", err.getvalue())

    def test_human_readable_output(self):
        code, out = run_cli("analyze", str(self.file))
        self.assertEqual(code, 0)
        self.assertIn("language: Portuguese", out)


if __name__ == "__main__":
    unittest.main()
