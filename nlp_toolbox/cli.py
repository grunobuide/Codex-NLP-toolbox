"""Command-line interface: transparent NLP baselines usable in pipelines.

Every subcommand reads a UTF-8 text file and prints either a human-readable
summary or, with ``--json``, machine-readable JSON (stable keys, UTF-8).
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from nlp_toolbox.languages import LANGUAGE_OPTIONS, get_language_config
from nlp_toolbox.tools import (
    READABILITY_FORMULAS,
    analyze_text,
    collocations,
    detect_language_details,
    extract_keywords,
    filter_tokens,
    kwic,
    porter_stem,
    readability_score,
    split_sentences,
    tfidf_keywords,
    tokenize_text,
    zipf_table,
)


def _read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def _resolve_language(text: str, requested: str) -> tuple[str, bool]:
    """Return (language, fallback_used). ``auto`` triggers detection."""
    if requested != "auto":
        return requested, False
    details = detect_language_details(text)
    return details.language, details.fallback


def _emit(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    for key, value in payload.items():
        if isinstance(value, list):
            print(f"{key}:")
            for row in value:
                print(f"  {row}")
        else:
            print(f"{key}: {value}")


def _cmd_analyze(args: argparse.Namespace) -> int:
    text = _read_text(args.file)
    language, fallback = _resolve_language(text, args.lang)
    config = get_language_config(language)
    sentences = split_sentences(text)
    tokens = tokenize_text(text)
    content_tokens = filter_tokens(tokens, config)
    formula = READABILITY_FORMULAS.get(language, READABILITY_FORMULAS["English"])
    payload: dict[str, Any] = {
        "file": args.file,
        "language": language,
        "language_detection_fallback": fallback,
        "stats": analyze_text(text, tokens, sentences),
        "readability": {
            "formula": formula.name,
            "score": readability_score(text, tokens, sentences, language),
        },
        "keywords": extract_keywords(content_tokens, config, top_k=args.top_k),
    }
    _emit(payload, args.json)
    return 0


def _cmd_keywords(args: argparse.Namespace) -> int:
    text = _read_text(args.file)
    language, _ = _resolve_language(text, args.lang)
    config = get_language_config(language)
    tokens = filter_tokens(tokenize_text(text), config)
    if args.method == "tfidf":
        sentence_docs = [
            filter_tokens(tokenize_text(sentence), config) for sentence in split_sentences(text)
        ]
        keywords: list[dict[str, Any]] = list(tfidf_keywords(sentence_docs, top_k=args.top_k))
    else:
        keywords = list(extract_keywords(tokens, config, top_k=args.top_k))
    _emit(
        {"file": args.file, "language": language, "method": args.method, "keywords": keywords},
        args.json,
    )
    return 0


def _cmd_kwic(args: argparse.Namespace) -> int:
    text = _read_text(args.file)
    tokens = tokenize_text(text, lowercase=False)
    matches = kwic(tokens, args.keyword, window=args.window, max_matches=args.max_matches)
    _emit({"file": args.file, "keyword": args.keyword, "matches": matches}, args.json)
    return 0


def _cmd_zipf(args: argparse.Namespace) -> int:
    text = _read_text(args.file)
    table = zipf_table(tokenize_text(text), top_k=args.top_k)
    _emit({"file": args.file, "table": table}, args.json)
    return 0


def _cmd_collocations(args: argparse.Namespace) -> int:
    text = _read_text(args.file)
    tokens = tokenize_text(text)
    rows = collocations(tokens, min_count=args.min_count, top_k=args.top_k)
    _emit({"file": args.file, "collocations": rows}, args.json)
    return 0


def _cmd_stem(args: argparse.Namespace) -> int:
    stems = [{"word": word, "stem": porter_stem(word)} for word in args.words]
    _emit({"stems": stems}, args.json)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codex-nlp",
        description="Transparent NLP baselines: analyze text files from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    languages = ["auto", *LANGUAGE_OPTIONS]

    analyze = subparsers.add_parser("analyze", help="Full profile: stats, readability, keywords")
    analyze.add_argument("file")
    analyze.add_argument("--lang", choices=languages, default="auto")
    analyze.add_argument("--top-k", type=int, default=10)
    analyze.add_argument("--json", action="store_true")
    analyze.set_defaults(handler=_cmd_analyze)

    keywords = subparsers.add_parser("keywords", help="Keyword extraction (freq or tfidf)")
    keywords.add_argument("file")
    keywords.add_argument("--method", choices=["freq", "tfidf"], default="freq")
    keywords.add_argument("--lang", choices=languages, default="auto")
    keywords.add_argument("--top-k", type=int, default=10)
    keywords.add_argument("--json", action="store_true")
    keywords.set_defaults(handler=_cmd_keywords)

    kwic_parser = subparsers.add_parser("kwic", help="Keyword-in-context concordance")
    kwic_parser.add_argument("file")
    kwic_parser.add_argument("keyword")
    kwic_parser.add_argument("--window", type=int, default=5)
    kwic_parser.add_argument("--max-matches", type=int, default=50)
    kwic_parser.add_argument("--json", action="store_true")
    kwic_parser.set_defaults(handler=_cmd_kwic)

    zipf = subparsers.add_parser("zipf", help="Rank-frequency (Zipf) table")
    zipf.add_argument("file")
    zipf.add_argument("--top-k", type=int, default=50)
    zipf.add_argument("--json", action="store_true")
    zipf.set_defaults(handler=_cmd_zipf)

    colloc = subparsers.add_parser("collocations", help="Bigram collocations (PMI + LLR)")
    colloc.add_argument("file")
    colloc.add_argument("--min-count", type=int, default=3)
    colloc.add_argument("--top-k", type=int, default=20)
    colloc.add_argument("--json", action="store_true")
    colloc.set_defaults(handler=_cmd_collocations)

    stem = subparsers.add_parser("stem", help="Porter-stem English words")
    stem.add_argument("words", nargs="+")
    stem.add_argument("--json", action="store_true")
    stem.set_defaults(handler=_cmd_stem)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result: int = args.handler(args)
    except FileNotFoundError as error:
        print(f"error: file not found: {error.filename}", file=sys.stderr)
        return 2
    return result


if __name__ == "__main__":
    sys.exit(main())
