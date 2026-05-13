#!/usr/bin/env python3
"""propose-rule-citations.py — propose `> Real-world example:` lines for rules.

Walks `auditor/exemplars/*.md`, builds a `rule_id → [exemplar]` map,
and proposes an edit to `skills/nlpm/rules/SKILL.md` that inserts a
`> Real-world example: [slug](relpath), [slug](relpath)` line after
each rule whose body doesn't already cite its exemplars.

This is a PROPOSAL generator — it writes a unified diff to stdout or a
file, OR it writes the edited file to a separate location. It does NOT
modify `skills/nlpm/rules/SKILL.md` directly. The human-gated path:

    1. Weekly cron (`auditor-cite-exemplars.yml`) runs this script.
    2. If the diff is non-empty, it opens a PR for human review.
    3. xiaolai reviews + merges (mirrors `auditor-refine-rules.yml`).

We never auto-merge edits to `skills/nlpm/rules/` — that file is the
load-bearing artifact that powers every audit, and an unreviewed
rewrite would silently corrupt every future audit's calibration.

Exit codes:
  0 — proposal emitted (may be empty / no-op)
  1 — would-make-changes (only with --check, mirrors gallery script)
  2 — internal error (rules file unreadable)

Usage:
  python3 auditor/scripts/propose-rule-citations.py              # print diff to stdout
  python3 auditor/scripts/propose-rule-citations.py --apply      # write edits in place (used by the cite-exemplars workflow before opening the PR)
  python3 auditor/scripts/propose-rule-citations.py --check      # exit 1 if any edits would be made
  python3 auditor/scripts/propose-rule-citations.py --self-test
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXEMPLARS_DIR = REPO_ROOT / "auditor" / "exemplars"
RULES_PATH = REPO_ROOT / "skills" / "nlpm" / "rules" / "SKILL.md"
# Relative path from skills/nlpm/rules/SKILL.md to an exemplar — used in the
# inserted citation links so they resolve correctly when read from the rules file.
EXEMPLAR_RELPATH_FROM_RULES = "../../../auditor/exemplars"


def parse_exemplar_frontmatter(text: str) -> dict[str, object]:
    """Minimal copy of build-exemplar-gallery.py's parser — kept local so the
    script is single-file and stdlib-only."""
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        return {}
    fm = fm_match.group(1)
    out: dict[str, object] = {}
    for key in ("slug", "repo"):
        m = re.search(rf"^{key}:\s*([\S]+)", fm, re.MULTILINE)
        if m:
            out[key] = m.group(1).strip().strip('"').strip("'")
    in_list = False
    rules: list[str] = []
    for line in fm.splitlines():
        if re.match(r"^exemplifies:\s*$", line):
            in_list = True
            continue
        if not in_list:
            continue
        m = re.match(r"^[ \t]+-[ \t]+(R\d{2})\b", line)
        if m:
            rules.append(m.group(1))
            continue
        if line and not line.startswith((" ", "\t")):
            in_list = False
    out["exemplifies"] = rules
    return out


def build_rule_to_exemplars(exemplars_dir: Path) -> dict[str, list[tuple[str, str]]]:
    """Returns {rule_id: [(slug, filename), ...]} sorted by slug per rule."""
    by_rule: dict[str, list[tuple[str, str]]] = defaultdict(list)
    if not exemplars_dir.exists():
        return {}
    for path in sorted(exemplars_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        fm = parse_exemplar_frontmatter(text)
        slug = fm.get("slug") or path.stem
        for rid in fm.get("exemplifies") or []:
            by_rule[rid].append((str(slug), path.name))
    # Stable per-rule ordering
    return {rid: sorted(slugs) for rid, slugs in by_rule.items()}


# Marker convention for auto-inserted citation lines. Using an HTML comment
# anchor makes the lines machine-detectable for future re-runs (so we know
# what we've already inserted and where to UPDATE vs. insert).
CITATION_BEGIN = "<!-- nlpm-exemplar-citation:begin -->"
CITATION_END = "<!-- nlpm-exemplar-citation:end -->"


def render_citation_block(slugs: list[tuple[str, str]]) -> str:
    """Render the `> Real-world example: [...]` line wrapped in markers."""
    links = ", ".join(
        f"[{slug}]({EXEMPLAR_RELPATH_FROM_RULES}/{fname})"
        for slug, fname in slugs
    )
    return f"{CITATION_BEGIN}\n> Real-world example: {links}\n{CITATION_END}"


def edit_rules_text(text: str, by_rule: dict[str, list[tuple[str, str]]]) -> str:
    """Return rules SKILL.md text with citation blocks updated.

    For each rule that has exemplars:
      - If a `nlpm-exemplar-citation:begin/end` block already exists
        immediately after the rule's body, REPLACE it (idempotent re-run
        keeps the block in sync as new exemplars land).
      - Otherwise, INSERT a new block right before the next rule heading
        (`**R\\d{2}\\.`) or section divider (`---`).
    """
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    # Scan and rebuild
    while i < len(lines):
        line = lines[i]
        m = re.match(r"\*\*(R\d{2})\.", line)
        if not m:
            out.append(line)
            i += 1
            continue

        rule_id = m.group(1)
        # Capture this rule's body until the next rule heading or `---`
        rule_start = i
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if re.match(r"\*\*R\d{2}\.", nxt):
                break
            # Be conservative: only stop on `---` if it's a section divider
            # (line is just `---\n` or `---`, no content)
            stripped = nxt.strip()
            if stripped == "---":
                break
            i += 1
        rule_end = i  # exclusive

        body = lines[rule_start:rule_end]

        # Detect existing citation block within this rule's body
        existing_block_start = None
        existing_block_end = None
        for j in range(len(body)):
            if body[j].strip() == CITATION_BEGIN:
                existing_block_start = j
            elif body[j].strip() == CITATION_END:
                existing_block_end = j
                break

        slugs = by_rule.get(rule_id)
        if slugs:
            new_block = render_citation_block(slugs) + "\n"
            new_block_lines = [l + "\n" if not l.endswith("\n") else l
                               for l in new_block.split("\n") if l != ""]
            # Reconstruct as exact 3-line block ending with newline
            new_block_lines = [
                CITATION_BEGIN + "\n",
                f"> Real-world example: " + ", ".join(
                    f"[{slug}]({EXEMPLAR_RELPATH_FROM_RULES}/{fname})"
                    for slug, fname in slugs
                ) + "\n",
                CITATION_END + "\n",
            ]
            if existing_block_start is not None and existing_block_end is not None:
                # Replace the existing block
                replacement = body[:existing_block_start] + new_block_lines + body[existing_block_end + 1:]
                out.extend(replacement)
            else:
                # Insert before trailing blank line(s) at end of body
                trailing_blanks = 0
                for k in range(len(body) - 1, -1, -1):
                    if body[k].strip() == "":
                        trailing_blanks += 1
                    else:
                        break
                insertion_pt = len(body) - trailing_blanks
                # Add a blank line separator before the block if not already present
                pre = body[:insertion_pt]
                post = body[insertion_pt:]
                if pre and pre[-1].strip() != "":
                    pre = pre + ["\n"]
                out.extend(pre + new_block_lines + post)
        else:
            # No exemplars for this rule. Remove any stale block if present.
            if existing_block_start is not None and existing_block_end is not None:
                # Drop the stale block (and one trailing blank line if present)
                clean = body[:existing_block_start] + body[existing_block_end + 1:]
                # Trim possibly-orphan blank-line pair around the removed block
                # (light touch — don't aggressively reflow)
                out.extend(clean)
            else:
                out.extend(body)

    return "".join(out)


def make_unified_diff(original: str, edited: str, label: str) -> str:
    return "".join(difflib.unified_diff(
        original.splitlines(keepends=True),
        edited.splitlines(keepends=True),
        fromfile=f"a/{label}",
        tofile=f"b/{label}",
    ))


def self_test() -> int:
    """Inline tests for edit_rules_text (insert, replace, remove cases)."""
    sample_rules = """\
# The Rules

**R04. Description is a trigger, not a summary.** 3+ specific action phrases matching real user queries.

Bad: "Helpful skill."
Good: "Use when debugging React re-renders, fixing hook deps."

**R05. Under 500 lines.** Over 500 = context bloat.

**R06. Code examples must be runnable.** Not pseudocode.

---

> Scope note: end of file.
"""

    # Case 1: insert citation for R04 + R06
    by_rule = {
        "R04": [("foo-bar", "foo-bar.md")],
        "R06": [("alpha-x", "alpha-x.md"), ("beta-y", "beta-y.md")],
    }
    edited = edit_rules_text(sample_rules, by_rule)
    assert "nlpm-exemplar-citation:begin" in edited, edited
    assert edited.count(CITATION_BEGIN) == 2, edited.count(CITATION_BEGIN)
    assert "[foo-bar]" in edited
    assert "[alpha-x]" in edited and "[beta-y]" in edited
    # R05 must NOT have a citation block
    r05_block = edited.split("**R05.")[1].split("**R06.")[0]
    assert CITATION_BEGIN not in r05_block, "R05 should not have a citation"

    # Case 2: idempotent re-run
    edited_again = edit_rules_text(edited, by_rule)
    assert edited == edited_again, "edit_rules_text must be idempotent"

    # Case 3: updating with new exemplar replaces (not stacks) the block
    by_rule_updated = {
        "R04": [("foo-bar", "foo-bar.md"), ("new-one", "new-one.md")],
        "R06": [("alpha-x", "alpha-x.md"), ("beta-y", "beta-y.md")],
    }
    edited2 = edit_rules_text(edited, by_rule_updated)
    assert edited2.count(CITATION_BEGIN) == 2, "still exactly 2 blocks (no stacking)"
    assert "[new-one]" in edited2

    # Case 4: when a rule loses all exemplars, the stale block is removed
    by_rule_drop_r04 = {
        "R06": [("alpha-x", "alpha-x.md")],
    }
    edited3 = edit_rules_text(edited, by_rule_drop_r04)
    assert edited3.count(CITATION_BEGIN) == 1
    assert "[foo-bar]" not in edited3
    assert "[alpha-x]" in edited3

    # Case 5: empty input — no change
    assert edit_rules_text(sample_rules, {}) == sample_rules

    print("self-test PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    p.add_argument("--apply", action="store_true",
                   help="Write edits in place (used by the cite-exemplars workflow)")
    p.add_argument("--check", action="store_true",
                   help="Exit 1 if any edits would be made")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--rules-path", type=Path, default=RULES_PATH)
    p.add_argument("--exemplars-dir", type=Path, default=EXEMPLARS_DIR)
    args = p.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.rules_path.exists():
        print(f"ERROR: rules file not found: {args.rules_path}", file=sys.stderr)
        return 2

    by_rule = build_rule_to_exemplars(args.exemplars_dir)
    original = args.rules_path.read_text()
    edited = edit_rules_text(original, by_rule)

    if original == edited:
        if args.check:
            print("OK: rules file is in sync with exemplars (no citations to add/update/remove)")
        else:
            print("No changes proposed — rules file is already in sync.")
        return 0

    if args.check:
        print("DRIFT: rules file would be updated. Run without --check, or via the cite-exemplars workflow.", file=sys.stderr)
        # Also print the diff so CI logs show what's pending
        print(make_unified_diff(original, edited, str(args.rules_path)), file=sys.stderr)
        return 1

    if args.apply:
        args.rules_path.write_text(edited)
        print(f"wrote {args.rules_path}")
        return 0

    # Default: print diff to stdout
    print(make_unified_diff(original, edited, str(args.rules_path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
