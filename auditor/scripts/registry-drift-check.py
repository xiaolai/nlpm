#!/usr/bin/env python3
"""Deterministic vocabulary-drift gate: registry-declared pairs only.

Replaces open-ended LLM drift clustering as the hard vocab-integrity
gate. The LLM clusterer (agents/vocab-drift-scanner.md) surfaces drift
candidates a human curates into the registry; it is advisory. This
script is the enforcement layer: it greps the corpus for terms the
registry itself declares deprecated, and nothing else.

Why: a hard release gate needs a bounded rule set, reproducible output,
and a stable definition of "clean". Five consecutive gate runs on one
release PR each produced a different cluster set (see nlpm PR #708) —
an open-ended judge cannot certify a corpus clean because its bar moves
every run. This scanner is byte-deterministic: same corpus + same
registry => same findings.

Contract:
  - Only terms listed in a pair's `enforce_terms:` hard-fail. Terms
    stay advisory until they grep clean against the current corpus
    (common English words like "file" or "list" can never be
    mechanically enforced; they stay advisory forever).
  - Matches are word-boundary, case-insensitive, scope-aware: a file is
    checked only against pairs whose registry scope covers it (the
    auditor scope canonicalizes `validate`, which the internal scope
    deprecates — per-scope application is what keeps that coherent).
  - `sanctioned:` entries in registry.yaml suppress specific
    (term, path-glob) pairs with a recorded reason — the machine-readable
    counterpart of the SKILL.md sanctioned-homonyms table.
  - A malformed registry (unreadable, duplicate canonical, enforced pair
    with no deprecated terms, sanctioned entry missing term/path/reason)
    fails the run — a gate that silently skips its rulebook is not a gate.

Usage:
  registry-drift-check.py [--root DIR] [--report-all] [--self-test]

Exit codes: 0 clean, 1 enforced findings (or malformed registry),
2 usage error.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("registry-drift-check: PyYAML required", file=sys.stderr)
    sys.exit(2)

REGISTRY_PATH = "skills/nlpm/vocabulary/registry.yaml"

# The gate's enumerated artifact set (mirrors the score gate's targets).
# Codex mirrors are excluded: generated from the Claude tree.
SCAN_GLOBS = [
    "commands/*.md",
    "commands/shared/*.md",
    "agents/*.md",
    "skills/nlpm/*/SKILL.md",
    "AGENTS.md",
]

# Registry scope name -> path prefixes it covers (from registry.yaml's
# scope declarations). A file outside every listed prefix for a scope is
# not checked against that scope's pairs.
SCOPE_PREFIXES = {
    "internal": ("commands/", "agents/", "skills/", "bin/", "scripts/", "AGENTS.md", "CLAUDE.md"),
    "auditor": ("auditor/", ".github/workflows/"),
    # Noun scopes apply corpus-wide: artifact-class and output-class nouns
    # name nlpm's own objects wherever they appear.
    "artifact_class": ("",),
    "output_class": ("",),
}


class RegistryError(Exception):
    pass


def load_registry(root: Path):
    path = root / REGISTRY_PATH
    try:
        data = yaml.safe_load(path.read_text())
    except Exception as e:
        raise RegistryError(f"unreadable registry {path}: {e}")
    if not isinstance(data, dict):
        raise RegistryError("registry root is not a mapping")

    pairs = []       # (scope, canonical, deprecated_terms, enforce)
    seen = set()

    def walk(node, scope):
        if isinstance(node, dict):
            if "canonical" in node:
                canonical = node["canonical"]
                key = (scope, canonical)
                if key in seen:
                    raise RegistryError(f"duplicate canonical {canonical!r} in scope {scope!r}")
                seen.add(key)
                dep = node.get("deprecated") or []
                enforce_terms = node.get("enforce_terms") or []
                unknown = [t for t in enforce_terms if t not in dep]
                if unknown:
                    raise RegistryError(
                        f"{canonical!r} ({scope}) enforces terms not in its deprecated list: {unknown}")
                if dep:
                    pairs.append((scope, canonical, list(dep), list(enforce_terms)))
                return
            for k, v in node.items():
                walk(v, k if scope is None else scope)
        elif isinstance(node, list):
            for item in node:
                walk(item, scope)

    for top, sub in data.items():
        if top == "sanctioned":
            continue
        walk(sub, None if top in ("verbs", "nouns") else top)

    sanctioned = data.get("sanctioned") or []
    for entry in sanctioned:
        if not isinstance(entry, dict) or not all(k in entry for k in ("term", "path", "reason")):
            raise RegistryError(f"sanctioned entry missing term/path/reason: {entry!r}")

    return pairs, sanctioned


def scope_covers(scope: str, relpath: str) -> bool:
    prefixes = SCOPE_PREFIXES.get(scope)
    if prefixes is None:
        # Unknown scope name: enforce nothing, but do not silently drop —
        # surface as a registry problem.
        raise RegistryError(f"registry declares unknown scope {scope!r}")
    return any(relpath.startswith(p) or p == "" for p in prefixes)


def is_sanctioned(sanctioned, term: str, relpath: str) -> bool:
    return any(
        e["term"].lower() == term.lower() and fnmatch.fnmatch(relpath, e["path"])
        for e in sanctioned
    )


def scan(root: Path, pairs, sanctioned, report_all: bool):
    findings = []
    files = sorted({p for g in SCAN_GLOBS for p in root.glob(g) if p.is_file()})
    for f in files:
        rel = f.relative_to(root).as_posix()
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        for scope, canonical, deprecated, enforce_terms in pairs:
            if not (enforce_terms or report_all):
                continue
            if not scope_covers(scope, rel):
                continue
            for term in deprecated:
                enforced = term in enforce_terms
                if not (enforced or report_all):
                    continue
                rx = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
                for lineno, line in enumerate(lines, 1):
                    if not rx.search(line):
                        continue
                    if is_sanctioned(sanctioned, term, rel):
                        continue
                    findings.append({
                        "file": rel, "line": lineno, "term": term,
                        "canonical": canonical, "scope": scope,
                        "enforced": enforced, "text": line.strip()[:160],
                    })
    return findings


FIXTURE_REGISTRY = """\
verbs:
  internal:
    - canonical: check
      deprecated: [flurb]
      enforce_terms: [flurb]
    - canonical: score
      deprecated: [grumble]
nouns:
  output_class:
    - canonical: finding
      deprecated: [snag]
      enforce_terms: [snag]
sanctioned:
  - term: snag
    path: "commands/teaching.md"
    reason: quoted as data in a drift-teaching example
"""

FIXTURES = {
    # positive: enforced term in scope -> finding
    "commands/dirty.md": "Run the flurb pass over every artifact.\n",
    # negative: sanctioned (term, path) -> suppressed
    "commands/teaching.md": "Example of drift: calling a finding a snag.\n",
    # negative: non-enforced pair -> advisory only
    "agents/advisory.md": "The grumble step is optional.\n",
    # negative: word-boundary — "flurbish" must not match "flurb"
    "commands/boundary.md": "The flurbish quality is unrelated.\n",
}


def self_test() -> int:
    failures = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "skills/nlpm/vocabulary").mkdir(parents=True)
        (root / REGISTRY_PATH).write_text(FIXTURE_REGISTRY)
        for rel, content in FIXTURES.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)

        pairs, sanctioned = load_registry(root)
        hard = scan(root, pairs, sanctioned, report_all=False)
        soft = scan(root, pairs, sanctioned, report_all=True)

        if [(f["file"], f["term"]) for f in hard] != [("commands/dirty.md", "flurb")]:
            failures.append(f"hard findings wrong: {hard}")
        if not any(f["term"] == "grumble" and not f["enforced"] for f in soft):
            failures.append("advisory pair not reported in --report-all")
        if any(f["file"] == "commands/teaching.md" for f in soft):
            failures.append("sanctioned entry not suppressed")
        if any(f["file"] == "commands/boundary.md" for f in soft):
            failures.append("word boundary violated")

        # determinism: two scans, identical output
        if scan(root, pairs, sanctioned, True) != soft:
            failures.append("scan is not deterministic")

        # malformed registries must fail
        for bad, why in [
            ("verbs:\n  internal:\n    - canonical: check\n      deprecated: [x]\n      enforce_terms: [y]\n",
             "enforce_terms references a term outside deprecated"),
            ("verbs:\n  internal:\n    - canonical: x\n      deprecated: [y]\n    - canonical: x\n      deprecated: [z]\n",
             "duplicate canonical"),
            ("sanctioned:\n  - term: a\n", "sanctioned entry missing fields"),
        ]:
            (root / REGISTRY_PATH).write_text(bad)
            try:
                load_registry(root)
                failures.append(f"malformed registry accepted: {why}")
            except RegistryError:
                pass

    if failures:
        for f in failures:
            print(f"SELF-TEST FAIL: {f}", file=sys.stderr)
        return 1
    print("registry-drift-check.py self-tests: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--report-all", action="store_true",
                    help="also print advisory (non-enforced) findings; never affects exit code")
    ap.add_argument("--json", action="store_true", help="JSONL output")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    root = Path(args.root).resolve()
    try:
        pairs, sanctioned = load_registry(root)
        findings = scan(root, pairs, sanctioned, args.report_all)
    except RegistryError as e:
        print(f"::error::registry-drift-check: malformed registry — {e}", file=sys.stderr)
        return 1

    hard = [f for f in findings if f["enforced"]]
    for f in findings:
        tag = "error" if f["enforced"] else "notice"
        if args.json:
            print(json.dumps(f))
        else:
            print(f"::{tag} file={f['file']},line={f['line']}::"
                  f"deprecated term '{f['term']}' (canonical: '{f['canonical']}', "
                  f"scope: {f['scope']}): {f['text']}")
    print(f"registry-drift-check: {len(hard)} enforced finding(s), "
          f"{len(findings) - len(hard)} advisory", file=sys.stderr)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
