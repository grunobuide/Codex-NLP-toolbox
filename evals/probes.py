"""Robustness probes: measured behavior under degraded input.

Not benchmarks (no external gold beyond the frozen datasets) — these feed
docs/error-analysis.md with numbers instead of anecdotes.

Usage: ``uv run --group evals python -m evals.probes``
"""

from pathlib import Path

from evals.metrics import accuracy
from nlp_toolbox.tools import detect_language_details, detect_language_ngram

ROOT = Path(__file__).resolve().parent
NAME_TO_CODE = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
}


def langid_vs_length() -> list[tuple[str, float, float, float]]:
    """Toolbox language-ID accuracy when texts are truncated to k words."""
    rows = [
        line.split("\t")
        for line in (ROOT / "datasets" / "langid.tsv").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    gold = [r[0] for r in rows]
    results = []
    for k in (2, 4, 8, 16, None):
        texts = [" ".join(r[1].split()[:k]) if k else r[1] for r in rows]
        preds = [NAME_TO_CODE[detect_language_details(t).language] for t in texts]
        ngram_preds = [NAME_TO_CODE[detect_language_ngram(t)] for t in texts]
        fallback_rate = sum(1 for t in texts if detect_language_details(t).fallback) / len(texts)
        results.append(
            (
                f"first {k} words" if k else "full sentence",
                accuracy(gold, preds),
                accuracy(gold, ngram_preds),
                round(fallback_rate, 4),
            )
        )
    return results


def main() -> int:
    print("| Input | Hint-words accuracy | Char-ngrams accuracy | Hint fallback rate |")
    print("|---|---|---|---|")
    for label, acc, ngram_acc, fb in langid_vs_length():
        print(f"| {label} | {acc:.4f} | {ngram_acc:.4f} | {fb:.0%} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
