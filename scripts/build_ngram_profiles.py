"""Reproducibly (re)build the character n-gram language profiles.

Fetches plain-text extracts of three Wikipedia articles per language (the
article on the language itself, "Literature", and "Linguistics", each in that
language's Wikipedia), builds a top-N character-trigram profile with the exact
same normalization used at detection time (``nlp_toolbox.tools.build_ngram_profile``),
and writes:

* ``nlp_toolbox/resources/ngram_profiles/<code>.txt`` — the ranked profile;
* ``nlp_toolbox/resources/ngram_profiles/manifest.json`` — full provenance:
  per-article resolved title, canonical URL, revision id and revision timestamp
  (captured at fetch time), plus the SHA-256 of each generated profile file and
  the UTC build timestamp.

Wikipedia article text is licensed CC BY-SA 4.0; the derived profiles inherit
that license (see ``NOTICE`` and ``nlp_toolbox/resources/ngram_profiles/PROVENANCE.md``).
This project's *code* is MIT; the two licenses are kept separate on purpose.

Usage:
    python -m scripts.build_ngram_profiles            # rebuild all languages
    python -m scripts.build_ngram_profiles --check    # dry run: fetch + report only

Note: rebuilding fetches *current* Wikipedia revisions, so the resulting
profiles may differ slightly from the frozen files shipped in the package.
That is a deliberate, versioned change — commit the new profiles together with
the updated manifest and re-run the evaluation harness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from nlp_toolbox.tools import build_ngram_profile

PROFILE_SIZE = 300
_REPO_ROOT = Path(__file__).resolve().parent.parent
_PROFILE_DIR = _REPO_ROOT / "nlp_toolbox" / "resources" / "ngram_profiles"

# (language name, wiki subdomain code, [article titles in that language]).
# Titles are the canonical article names; ``redirects=1`` resolves minor
# variants and the manifest records whatever the API returns as the final title.
ARTICLES: dict[str, tuple[str, list[str]]] = {
    "English": ("en", ["English language", "Literature", "Linguistics"]),
    "Spanish": ("es", ["Idioma español", "Literatura", "Lingüística"]),
    "French": ("fr", ["Français", "Littérature", "Linguistique"]),
    "German": ("de", ["Deutsche Sprache", "Literatur", "Sprachwissenschaft"]),
    "Italian": ("it", ["Lingua italiana", "Letteratura", "Linguistica"]),
    "Portuguese": ("pt", ["Língua portuguesa", "Literatura", "Linguística"]),
}

_USER_AGENT = "Codex-NLP-toolbox profile builder (https://github.com/grunobuide/Codex-NLP-toolbox)"


def _api_url(code: str, titles: list[str]) -> str:
    params = {
        "action": "query",
        "prop": "extracts|revisions",
        "explaintext": "1",
        "exlimit": "max",
        "rvprop": "ids|timestamp",
        "redirects": "1",
        "format": "json",
        "formatversion": "2",
        "titles": "|".join(titles),
    }
    return f"https://{code}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)


def _fetch(code: str, titles: list[str]) -> list[dict[str, object]]:
    """Return one record per article: title, url, revid, timestamp, text, chars."""
    request = urllib.request.Request(_api_url(code, titles), headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 (trusted host)
        data = json.loads(response.read().decode("utf-8"))
    pages = {page["title"]: page for page in data["query"]["pages"]}
    records: list[dict[str, object]] = []
    for page in pages.values():
        if page.get("missing"):
            raise SystemExit(f"error: article not found on {code}.wikipedia: {page['title']!r}")
        title = page["title"]
        revision = page["revisions"][0]
        slug = urllib.parse.quote(title.replace(" ", "_"))
        records.append(
            {
                "title": title,
                "url": f"https://{code}.wikipedia.org/wiki/{slug}",
                "revid": revision["revid"],
                "timestamp": revision["timestamp"],
                "text": page.get("extract", ""),
                "chars": len(page.get("extract", "")),
            }
        )
    return records


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(check_only: bool) -> int:
    manifest: dict[str, object] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profile_size": PROFILE_SIZE,
        "method": "Cavnar & Trenkle (1994), N-gram-based text categorization",
        "normalization": "lowercase; non-letter runs collapsed to '_'; trigrams with >=1 letter",
        "source_license": "CC BY-SA 4.0 (Wikipedia article text)",
        "languages": {},
    }
    languages_manifest: dict[str, object] = manifest["languages"]  # type: ignore[assignment]
    for language, (code, titles) in ARTICLES.items():
        records = _fetch(code, titles)
        combined = "\n\n".join(str(record["text"]) for record in records)
        profile = build_ngram_profile(combined, size=PROFILE_SIZE)
        out_path = _PROFILE_DIR / f"{code}.txt"
        if not check_only:
            out_path.write_text("\n".join(profile) + "\n", encoding="utf-8")
        languages_manifest[language] = {
            "code": code,
            "wikipedia": f"{code}.wikipedia.org",
            "articles": [
                {key: record[key] for key in ("title", "url", "revid", "timestamp", "chars")}
                for record in records
            ],
            "total_chars": sum(int(record["chars"]) for record in records),
            "profile_file": f"{code}.txt",
            "profile_sha256": _sha256(out_path) if out_path.exists() else None,
        }
        total = sum(int(record["chars"]) for record in records)
        print(
            f"{language:11s} {code}  {len(profile)} trigrams  {total:>7,d} chars",
            file=sys.stderr,
        )

    if not check_only:
        (_PROFILE_DIR / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print("wrote manifest.json", file=sys.stderr)
    else:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fetch and report provenance without overwriting profile files.",
    )
    args = parser.parse_args(argv)
    return build(check_only=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
