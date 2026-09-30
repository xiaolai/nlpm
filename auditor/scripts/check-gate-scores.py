#!/usr/bin/env python3
"""Assert the pre-release gate's LLM scores are complete and grounded.

The gate's LLM step writes a TSV with the header `file<TAB>score<TAB>quote`,
one row per artifact listed in the selection file. A bare "no score below the
minimum" check passed rows the model never earned: on two release PRs it wrote
100 for every file after reading almost none. This check makes each row cost a
read and fails closed on anything missing or malformed:

  - every listed file is scored exactly once, and no unlisted file is;
  - each score is an integer from 0 to 100 and at least --min;
  - each quote is at least MIN_QUOTE characters, and appears verbatim in the
    body of that file (below its frontmatter).

Prints GitHub annotations; exits 1 on any failure.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

MIN_QUOTE = 24
HEADER = ["file", "score", "quote"]


def body_of(text: str) -> str:
    """Return the text below a leading YAML frontmatter block, if any."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[end + 4:]
    return text


def check(root: Path, listed: list[str], rows: list[list[str]], minimum: int) -> list[str]:
    errors: list[str] = []
    seen: dict[str, int] = {}
    for n, cols in enumerate(rows, start=2):
        if len(cols) != 3:
            errors.append(f"::error::scores line {n}: expected 3 tab-separated columns, got {len(cols)}")
            continue
        file, score, quote = (c.strip() for c in cols)
        seen[file] = seen.get(file, 0) + 1
        if file not in listed:
            errors.append(f"::error file={file}::scored but not in the list of changed artifacts")
            continue
        if not score.isdigit() or not 0 <= int(score) <= 100:
            errors.append(f"::error file={file}::score {score!r} is not an integer from 0 to 100")
            continue
        if int(score) < minimum:
            errors.append(f"::error file={file}::score={score}/100 (release requires >= {minimum})")
        if len(quote) < MIN_QUOTE:
            errors.append(f"::error file={file}::quote must be at least {MIN_QUOTE} characters, got {len(quote)}")
            continue
        path = root / file
        if not path.is_file():
            errors.append(f"::error file={file}::file does not exist")
            continue
        if quote not in body_of(path.read_text(encoding="utf-8")):
            errors.append(f"::error file={file}::quote not found in the file's body: {quote[:80]!r}")
    for file, count in seen.items():
        if count > 1:
            errors.append(f"::error file={file}::scored more than once ({count} rows)")
    for file in listed:
        if file not in seen:
            errors.append(f"::error file={file}::listed as changed but not scored")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--list", type=Path, required=True, help="one repo-relative path per line")
    ap.add_argument("--scores", type=Path, required=True)
    ap.add_argument("--min", type=int, required=True)
    a = ap.parse_args()

    listed = [line.strip() for line in a.list.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not a.scores.is_file():
        print(f"::error::{a.scores} was not written; the LLM scoring step failed or skipped")
        return 1
    lines = a.scores.read_text(encoding="utf-8").splitlines()
    if not lines or [c.strip() for c in lines[0].split("\t")] != HEADER:
        print(f"::error::{a.scores} header must be {'<TAB>'.join(HEADER)!r}")
        return 1
    rows = [line.split("\t") for line in lines[1:] if line.strip()]

    errors = check(a.root, listed, rows, a.min)
    for e in errors:
        print(e)
    if errors:
        print(f"::error::Score gate FAILED: {len(errors)} problem(s) across {len(listed)} listed artifact(s).")
        return 1
    print(f"::notice::Score gate PASSED: {len(rows)} of {len(listed)} artifacts scored >= {a.min}, each with a verified quote.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
