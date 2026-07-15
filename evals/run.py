"""Run an evaluation task and write a reproducible JSON result.

Usage::

    uv run --group evals python -m evals.run --task langid
    uv run --group evals python -m evals.run --task sentiment

Each run records the git SHA, dataset SHA-256, package versions, and the
full confusion matrix, so any number in ``docs/benchmarks.md`` can be traced
to one JSON file and recomputed by hand from the matrix.
"""

import argparse
import datetime
import hashlib
import json
import subprocess
from collections.abc import Callable
from importlib.metadata import version
from pathlib import Path
from typing import Any

from evals.metrics import accuracy, confusion_matrix, macro_f1, sentence_prf
from nlp_toolbox.tools import (
    detect_language_details,
    detect_language_ngram,
    sentiment_analysis,
    split_sentences,
    tokenize_text,
)

ROOT = Path(__file__).resolve().parent
NAME_TO_CODE = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
}


def _read_tsv(path: Path) -> list[list[str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(line.split("\t"))
    return rows


def _git_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT, check=True
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def _evaluate(gold: list[str], systems: dict[str, list[str]]) -> dict[str, Any]:
    return {
        name: {
            "accuracy": accuracy(gold, preds),
            "macro_f1": macro_f1(gold, preds),
            "confusion": confusion_matrix(gold, preds),
        }
        for name, preds in systems.items()
    }


def task_langid() -> dict[str, Any]:
    from langdetect import DetectorFactory, detect  # noqa: PLC0415

    DetectorFactory.seed = 0
    dataset = ROOT / "datasets" / "langid.tsv"
    rows = _read_tsv(dataset)
    gold = [r[0] for r in rows]
    texts = [r[1] for r in rows]

    toolbox = [NAME_TO_CODE[detect_language_details(t).language] for t in texts]
    toolbox_ngram = [NAME_TO_CODE[detect_language_ngram(t)] for t in texts]

    def _ld(text: str) -> str:
        try:
            return str(detect(text))
        except Exception:
            return "error"

    baseline = [_ld(t) for t in texts]
    return {
        "task": "language identification",
        "dataset": _dataset_info(dataset, len(rows)),
        "systems": _evaluate(
            gold,
            {
                "toolbox hint-words": toolbox,
                "toolbox char-ngrams": toolbox_ngram,
                f"langdetect {version('langdetect')}": baseline,
            },
        ),
    }


def task_sentiment() -> dict[str, Any]:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # noqa: PLC0415

    dataset = ROOT / "datasets" / "sentiment_en.tsv"
    rows = _read_tsv(dataset)
    gold = [r[0] for r in rows]
    texts = [r[2] for r in rows]

    def _toolbox(text: str) -> str:
        score = sentiment_analysis(tokenize_text(text))["score"]
        return "1" if score > 0 else "0"

    analyzer = SentimentIntensityAnalyzer()

    def _vader(text: str) -> str:
        return "1" if analyzer.polarity_scores(text)["compound"] > 0 else "0"

    zero_evidence = sum(
        1
        for t in texts
        if sentiment_analysis(tokenize_text(t))["positive"] == 0
        and sentiment_analysis(tokenize_text(t))["negative"] == 0
    )
    result = {
        "task": "binary sentiment (English)",
        "dataset": _dataset_info(dataset, len(rows)),
        "systems": _evaluate(
            gold,
            {
                "toolbox lexicon": [_toolbox(t) for t in texts],
                f"VADER {version('vaderSentiment')}": [_vader(t) for t in texts],
            },
        ),
    }
    result["systems"]["toolbox lexicon"]["zero_evidence_fraction"] = round(
        zero_evidence / len(texts), 4
    )
    return result


def _dataset_info(path: Path, n: int) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT.parent)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "n": n,
    }


def task_segmentation() -> dict[str, Any]:
    import pysbd  # noqa: PLC0415

    dataset = ROOT / "datasets" / "segmentation_en.txt"
    gold_sentences = [
        line.strip() for line in dataset.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    # deterministic paragraphs of 3 gold sentences joined by single spaces
    paragraphs = [
        (" ".join(gold_sentences[i : i + 3]), gold_sentences[i : i + 3])
        for i in range(0, len(gold_sentences), 3)
    ]
    segmenter = pysbd.Segmenter(language="en", clean=False)
    all_gold: list[str] = []
    toolbox_pred: list[str] = []
    pysbd_pred: list[str] = []
    for paragraph, gold in paragraphs:
        all_gold.extend(gold)
        toolbox_pred.extend(split_sentences(paragraph))
        pysbd_pred.extend(s.strip() for s in segmenter.segment(paragraph))
    return {
        "task": "sentence segmentation (English, UD-EWT gold)",
        "dataset": _dataset_info(dataset, len(gold_sentences)),
        "systems": {
            "toolbox regex": sentence_prf(all_gold, toolbox_pred),
            f"pysbd {version('pysbd')}": sentence_prf(all_gold, pysbd_pred),
        },
    }


TASKS: dict[str, Callable[[], dict[str, Any]]] = {
    "langid": task_langid,
    "sentiment": task_sentiment,
    "segmentation": task_segmentation,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=sorted(TASKS), required=True)
    parser.add_argument("--out", default=str(ROOT / "results"))
    args = parser.parse_args()

    payload = TASKS[args.task]()
    payload["git_sha"] = _git_sha()
    payload["timestamp_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat(
        timespec="seconds"
    )
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{args.task}.json"
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_file}")
    for name, scores in payload["systems"].items():
        summary = " ".join(
            f"{key}={value}" for key, value in scores.items() if isinstance(value, int | float)
        )
        print(f"  {name}: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
