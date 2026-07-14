import unittest

from evals.metrics import accuracy, confusion_matrix, macro_f1


class TestMetrics(unittest.TestCase):
    """Hand-computed examples: gold = [a, a, b, b], pred = [a, b, b, b]."""

    def setUp(self):
        self.gold = ["a", "a", "b", "b"]
        self.pred = ["a", "b", "b", "b"]

    def test_accuracy(self):
        self.assertEqual(accuracy(self.gold, self.pred), 0.75)

    def test_confusion_matrix(self):
        self.assertEqual(
            confusion_matrix(self.gold, self.pred),
            {"a": {"a": 1, "b": 1}, "b": {"a": 0, "b": 2}},
        )

    def test_macro_f1(self):
        # class a: P=1/1, R=1/2, F1=2/3 ; class b: P=2/3, R=2/2, F1=0.8
        # macro = (0.6667 + 0.8) / 2 = 0.7333
        self.assertEqual(macro_f1(self.gold, self.pred), 0.7333)

    def test_unseen_predicted_label_in_confusion(self):
        matrix = confusion_matrix(["a"], ["c"])
        self.assertEqual(matrix, {"a": {"a": 0, "c": 1}})

    def test_macro_f1_ignored_class_punished(self):
        # system never predicts b: accuracy 0.5 but macro-F1 = (0.6667+0)/2
        gold = ["a", "b"]
        pred = ["a", "a"]
        self.assertEqual(accuracy(gold, pred), 0.5)
        self.assertEqual(macro_f1(gold, pred), 0.3333)

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            accuracy(["a"], [])


if __name__ == "__main__":
    unittest.main()
