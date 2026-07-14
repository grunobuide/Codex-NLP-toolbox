"""Evaluation metrics implemented from scratch, hand-checkable.

No dependency on sklearn on purpose: every number in the benchmarks can be
recomputed with pencil and paper from the confusion matrix.
"""


def accuracy(gold: list[str], predicted: list[str]) -> float:
    """Fraction of exact matches. Requires equal-length, non-empty lists."""
    _check(gold, predicted)
    hits = sum(1 for g, p in zip(gold, predicted, strict=True) if g == p)
    return round(hits / len(gold), 4)


def confusion_matrix(gold: list[str], predicted: list[str]) -> dict[str, dict[str, int]]:
    """Nested dict: ``matrix[gold_label][predicted_label] = count``.

    Rows cover gold labels; columns include any label the system predicted.
    """
    _check(gold, predicted)
    labels = sorted(set(gold) | set(predicted))
    matrix = {g: dict.fromkeys(labels, 0) for g in sorted(set(gold))}
    for g, p in zip(gold, predicted, strict=True):
        matrix[g][p] += 1
    return matrix


def macro_f1(gold: list[str], predicted: list[str]) -> float:
    """Unweighted mean of per-class F1 over the gold label set.

    For each class c: precision = TP/(TP+FP), recall = TP/(TP+FN),
    F1 = 2PR/(P+R). Classes never predicted get F1 = 0 — macro-F1 punishes
    systems that ignore a class, which accuracy hides.
    """
    _check(gold, predicted)
    classes = sorted(set(gold))
    f1_scores = []
    for c in classes:
        tp = sum(1 for g, p in zip(gold, predicted, strict=True) if g == c and p == c)
        fp = sum(1 for g, p in zip(gold, predicted, strict=True) if g != c and p == c)
        fn = sum(1 for g, p in zip(gold, predicted, strict=True) if g == c and p != c)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        f1_scores.append(f1)
    return round(sum(f1_scores) / len(f1_scores), 4)


def _check(gold: list[str], predicted: list[str]) -> None:
    if not gold or len(gold) != len(predicted):
        raise ValueError("gold and predicted must be equal-length, non-empty lists")
