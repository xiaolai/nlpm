#!/usr/bin/env python3
"""validate-rule-ids.py — catch scorer drift between rubric and findings.

Parses `skills/nlpm/scoring/SKILL.md` for the per-artifact-type rule_id
catalog, then walks `auditor/audits/*.findings.jsonl` (or a path on argv)
and reports every NL-quality finding whose `rule_id` is not documented in
the rubric for that artifact's path category.

Catches two drift kinds:

  TYPE drift     — rule_id not allowed for this artifact's type.
                   E.g. R09 (agents-only) used on a SKILL.md, or R14
                   (commands-only) used on a skill.

  SEMANTIC drift — rule_id allowed for type, but the finding's pattern
                   shares no keywords with the rule_id's bold-imperative
                   title in rules/SKILL.md. E.g. R07 ("Scope note when
                   related skills exist") used with pattern
                   `missing-example-block` — type-valid but semantically
                   wrong. The 2026-05-13 lijigang/ljg-skills audit did
                   this 14 times. v0.8.16 catches it.

The 2026-05-13 baseline across 128 historical audit sidecars:
  861 type drifts, 126 semantic drifts, 3 format drifts (990 total).
Most type drifts are R11 misapplied to commands (R11 is agents-only)
or R14 to skills (commands-only). Most semantic drifts are R07 / R08
labeled on findings about something other than scope notes.

Penalty-amount drift (R07 used with -15 instead of -3) is not yet
checked structurally — the prompt fix in auditor/prompts/score-artifacts.md
is the only layer against that.

Exit codes:
  0 — no drift detected
  1 — drift detected (offending findings printed)
  2 — internal error (e.g., rubric not parseable)

Usage:
  python3 auditor/scripts/validate-rule-ids.py
  python3 auditor/scripts/validate-rule-ids.py auditor/audits/lijigang-ljg-skills.findings.jsonl
  python3 auditor/scripts/validate-rule-ids.py --rubric skills/nlpm/scoring/SKILL.md
  python3 auditor/scripts/validate-rule-ids.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUBRIC = REPO_ROOT / "skills" / "nlpm" / "scoring" / "SKILL.md"
DEFAULT_RULES = REPO_ROOT / "skills" / "nlpm" / "rules" / "SKILL.md"
DEFAULT_AUDITS_DIR = REPO_ROOT / "auditor" / "audits"

# Stopwords filtered from rule titles and finding patterns before keyword
# intersection. Most are generic English; the rest are NL-meta terms that
# appear across most rules and would over-match if kept ("missing", "no",
# "present"). The list errs on the side of LEAVING domain words in — better
# to over-flag false-positive drift than to miss real semantic mismatches.
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "do", "each", "every",
    "exist", "for", "from", "has", "have", "if", "in", "is", "it", "its",
    "must", "no", "not", "of", "on", "only", "or", "over", "per", "present",
    "should", "than", "that", "the", "their", "them", "there", "these",
    "this", "to", "too", "under", "until", "use", "valid", "when", "where",
    "which", "while", "who", "why", "will", "with", "without", "would",
    # NLPM-meta noise that shows up across many rules
    "missing", "field", "fields", "rule", "rules", "skill", "skills",
    "agent", "agents", "command", "commands", "block", "blocks",
}

ARTIFACT_TYPES = ("Skills", "Agents", "Commands", "Shared Partials", "Rules", "Hooks", "plugin.json", ".mcp.json", "CLAUDE.md", "Prompts", "Orchestration", "Plugins")

# Rule-id prefixes that are out-of-scope for the per-artifact rubric check —
# these are bug / cross-component / agent-only categories with their own
# vocabulary, not R-numbered quality rules.
NON_RUBRIC_PREFIXES = ("BUG-", "CC-", "SEC-", "AGENT-", "UNCLASSIFIED")

# Universal rules from skills/nlpm/rules/SKILL.md — apply to every artifact
# type and aren't listed in the per-artifact rubric tables. Treat them as
# always-valid so the validator focuses on actual misapplication.
UNIVERSAL_RULES = {
    "R01",  # No vague quantifiers without criteria
    "R02",  # Every line must earn its tokens
    "R03",  # Positive framing over prohibitions
    "R40",  # Five layers in order (prompts)
    "R41",  # Specify exact output format (prompts)
    "R42",  # Injection resistance (prompts)
    "R43",  # Parallel when independent (orchestration)
    "R44",  # QC gate (orchestration)
    "R45",  # Cost gate (orchestration)
    "R46",  # State file for resumability (orchestration)
    "R47",  # Max retry count (orchestration)
}


@dataclass
class Rubric:
    """Allowed rule_ids per artifact type, parsed from scoring/SKILL.md.

    `keywords_by_rule` is populated by parse_rules() from rules/SKILL.md
    and powers the semantic-drift check.
    """
    by_type: dict[str, set[str]] = field(default_factory=dict)
    all_rnumbers: set[str] = field(default_factory=set)
    keywords_by_rule: dict[str, set[str]] = field(default_factory=dict)

    def allowed_for_path(self, path: str) -> set[str]:
        """Return the rubric rule_ids valid for the artifact at this path."""
        artifact_type = classify_path(path)
        return self.by_type.get(artifact_type, set())


def parse_rubric(rubric_path: Path, rules_path: Path | None = None) -> Rubric:
    """Extract rule_ids per artifact type from the rubric markdown.

    If `rules_path` is provided (default: skills/nlpm/rules/SKILL.md), also
    populates `rubric.keywords_by_rule` for the semantic-drift check.
    """
    if not rubric_path.exists():
        raise FileNotFoundError(f"rubric not found: {rubric_path}")
    text = rubric_path.read_text()
    rubric = Rubric()
    rules_to_load = rules_path if rules_path is not None else DEFAULT_RULES
    rubric.keywords_by_rule = parse_rules(rules_to_load)

    # Sections look like:  ### Skills    then a table starting with | Rule |
    # The table runs until a blank line or the next heading.
    current_section: str | None = None
    in_table = False
    for line in text.splitlines():
        m = re.match(r"^### (.+)$", line)
        if m:
            section = m.group(1).strip()
            if section in ARTIFACT_TYPES:
                current_section = section
                rubric.by_type.setdefault(section, set())
                in_table = False
            else:
                current_section = None
            continue
        if current_section is None:
            continue
        if line.startswith("| Rule") or line.startswith("|------"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                in_table = False
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if not cells:
                continue
            rule_cell = cells[0]
            # Cells may contain `R04` or `R04 R05` or `--`. Extract every R-number.
            for rid in re.findall(r"R\d{2}", rule_cell):
                rubric.by_type[current_section].add(rid)
                rubric.all_rnumbers.add(rid)
    return rubric


def _singularize(token: str) -> str:
    """Crude English singularization so plural keywords match singular tokens.

    Conservative: only trims the most reliable plural endings; would
    otherwise produce false equivalences ("address" → "addres"). Domain
    over-flagging would be worse than under-flagging.
    """
    if len(token) <= 3:
        return token
    if token.endswith("ies") and len(token) > 4:
        return token[:-3] + "y"  # quantifiers → quantifier (no), but properties → property
    if token.endswith("ses") or token.endswith("xes"):
        return token[:-2]  # boxes → box
    if token.endswith("s") and not token.endswith("ss"):
        return token[:-1]  # examples → example, tools → tool
    return token


def _tokenize(text: str) -> set[str]:
    """Split a string into lowercase content tokens, dropping stopwords.

    Handles kebab-case, snake_case, camelCase, and natural text. Tokens
    shorter than 3 chars are dropped unconditionally — they're too generic
    to carry semantic signal. Output is normalized via _singularize so
    plurals and singulars match across the rubric ↔ findings boundary.
    """
    if not text:
        return set()
    text = re.sub(r"[-_/]+", " ", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    tokens = re.findall(r"[A-Za-z]{3,}", text.lower())
    return {_singularize(t) for t in tokens if t not in STOPWORDS}


def parse_rules(rules_path: Path) -> dict[str, set[str]]:
    """Extract keyword sets per rule_id from rules/SKILL.md bold imperatives.

    Each rule appears as `**R##. <Bold imperative>.**` followed by prose.
    We pull the bold imperative as the canonical semantic anchor — that's
    where the rule's domain words live. Keywords come from tokenizing
    that title.

    Example:
      `**R07. Scope note when related skills exist.**`
      → R07 keywords: {"scope", "note", "related"}  (skills/exist filtered)

      `**R06. Code examples must be runnable.**`
      → R06 keywords: {"code", "examples", "runnable"}
    """
    if not rules_path.exists():
        return {}
    text = rules_path.read_text()
    keywords: dict[str, set[str]] = {}
    # Match **R##. <title>.** — title runs until first period+space or **
    for match in re.finditer(r"\*\*(R\d{2})\.\s+([^*]+?)\.\*\*", text):
        rule_id = match.group(1)
        title = match.group(2)
        keywords.setdefault(rule_id, set()).update(_tokenize(title))
    return keywords


def classify_path(rel_path: str) -> str:
    """Map a relative artifact path to its rubric artifact-type label.

    Accepts both `agents/foo.md` and `path/to/agents/foo.md` shapes — the
    bare segments are anchored with `/` on both sides after normalization.
    """
    p = "/" + rel_path.lower().lstrip("/")
    if p.endswith("/skill.md") or "/skills/" in p:
        return "Skills"
    if "/agents/" in p:
        return "Agents"
    if "/commands/" in p:
        return "Commands"
    if "/rules/" in p:
        return "Rules"
    if p.endswith("/hooks.json"):
        return "Hooks"
    if p.endswith("/plugin.json"):
        return "plugin.json"
    if p.endswith("/.mcp.json"):
        return ".mcp.json"
    if p.endswith("/claude.md"):
        return "CLAUDE.md"
    return "Skills"  # default — most NL artifacts are skills


@dataclass
class Drift:
    """A single finding whose rule_id doesn't match the rubric.

    `kind` is one of:
      - `type`     — rule_id not allowed for this artifact's type
      - `semantic` — rule_id allowed for type, but the finding's pattern
                     shares no keywords with the rule_id's title (e.g.,
                     R07 ("scope note") used with pattern
                     "missing-example-block")
      - `format`   — rule_id doesn't match `R\\d{2}` and isn't an allowed prefix
    """
    audit_file: str
    line_no: int
    file: str
    rule_id: str
    penalty: int | None
    pattern: str
    expected_for_type: set[str]
    artifact_type: str
    description: str
    kind: str = "type"
    rule_keywords: set[str] = field(default_factory=set)
    pattern_tokens: set[str] = field(default_factory=set)

    def render(self) -> str:
        header = f"{self.audit_file}:{self.line_no}  {self.file}  [{self.kind} drift]"
        if self.kind == "semantic":
            return (
                f"{header}\n"
                f"  rule_id={self.rule_id}  penalty={self.penalty}  pattern={self.pattern}\n"
                f"  rule keywords: {sorted(self.rule_keywords) or '(none)'}\n"
                f"  pattern tokens: {sorted(self.pattern_tokens) or '(none)'}\n"
                f"  description={self.description[:120]}"
            )
        allowed_list = ", ".join(sorted(self.expected_for_type)) or "(none)"
        return (
            f"{header}\n"
            f"  rule_id={self.rule_id}  penalty={self.penalty}  pattern={self.pattern}\n"
            f"  artifact_type={self.artifact_type}; allowed R-numbers: {allowed_list}\n"
            f"  description={self.description[:120]}"
        )


def validate_findings(jsonl_path: Path, rubric: Rubric) -> list[Drift]:
    """Walk one .findings.jsonl, return all rule_id-vs-rubric mismatches."""
    drifts: list[Drift] = []
    for line_no, raw in enumerate(jsonl_path.read_text().splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError:
            continue  # invalid JSON is a separate concern, not this validator's
        if rec.get("category") != "nl_quality":
            continue
        rule_id = rec.get("rule_id", "")
        if not rule_id:
            continue
        if any(rule_id.startswith(p) for p in NON_RUBRIC_PREFIXES):
            continue
        if rule_id in UNIVERSAL_RULES:
            continue
        if not re.fullmatch(r"R\d{2}", rule_id):
            # rule_ids like "R04-extra" or anything non-canonical
            drifts.append(Drift(
                audit_file=jsonl_path.name,
                line_no=line_no,
                file=rec.get("file", "?"),
                rule_id=rule_id,
                penalty=rec.get("penalty"),
                pattern=rec.get("pattern", ""),
                expected_for_type=set(),
                artifact_type="?",
                description=rec.get("description", ""),
                kind="format",
            ))
            continue
        artifact_type = classify_path(rec.get("file", ""))
        allowed = rubric.by_type.get(artifact_type, set())
        if rule_id not in allowed:
            drifts.append(Drift(
                audit_file=jsonl_path.name,
                line_no=line_no,
                file=rec.get("file", "?"),
                rule_id=rule_id,
                penalty=rec.get("penalty"),
                pattern=rec.get("pattern", ""),
                expected_for_type=allowed,
                artifact_type=artifact_type,
                description=rec.get("description", ""),
                kind="type",
            ))
            continue  # one drift per finding — don't double-flag as semantic too

        # Semantic check: does the finding's pattern share at least one
        # keyword with the rule_id's bold-imperative title? Skips when
        # the rule has no known keywords (rules/SKILL.md unavailable or
        # the rule's title didn't yield any post-stopword tokens).
        rule_keywords = rubric.keywords_by_rule.get(rule_id, set())
        if not rule_keywords:
            continue
        pattern_text = rec.get("pattern", "") or ""
        pattern_tokens = _tokenize(pattern_text)
        # Many patterns name a generic class (e.g., "missing-frontmatter")
        # which after stopword filtering leaves no signal — don't false-flag
        # those. Require both sides to have content before declaring drift.
        if not pattern_tokens:
            continue
        if rule_keywords & pattern_tokens:
            continue
        drifts.append(Drift(
            audit_file=jsonl_path.name,
            line_no=line_no,
            file=rec.get("file", "?"),
            rule_id=rule_id,
            penalty=rec.get("penalty"),
            pattern=pattern_text,
            expected_for_type=allowed,
            artifact_type=artifact_type,
            description=rec.get("description", ""),
            kind="semantic",
            rule_keywords=rule_keywords,
            pattern_tokens=pattern_tokens,
        ))
    return drifts


def self_test() -> int:
    """Inline tests for parse_rubric, classify_path, and validate_findings."""
    import tempfile

    fake_rubric = """\
## Penalty Tables

### Skills

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| -- | `name` present | Missing | -25 |
| R04 | `description` present | Missing | -25 |
| R06 | `<example>` blocks | Zero examples | -10 |
| R07 | Scope note | Missing | -3 |

### Agents

| Rule | Check | Condition | Penalty |
|------|-------|-----------|---------|
| R09 | `<example>` blocks | Zero `<example>` blocks in the description | -15 |
| R11 | Tools | Unused | -3 |
"""
    fake_rules = """\
# The Rules

**R04. Description triggers Claude to dispatch the skill.** Long body here.

**R06. Code examples must be runnable.** Long body here.

**R07. Scope note when related skills exist.** Long body here.

**R09. `<example>` blocks are mandatory.** Long body here.

**R11. Tools follow least-privilege.** Long body here.
"""
    with tempfile.TemporaryDirectory() as td:
        rubric_path = Path(td) / "rubric.md"
        rubric_path.write_text(fake_rubric)
        rules_path = Path(td) / "rules.md"
        rules_path.write_text(fake_rules)
        rubric = parse_rubric(rubric_path, rules_path)
        assert rubric.by_type["Skills"] == {"R04", "R06", "R07"}, rubric.by_type
        assert rubric.by_type["Agents"] == {"R09", "R11"}, rubric.by_type
        assert "example" in rubric.keywords_by_rule.get("R06", set()), rubric.keywords_by_rule
        assert "scope" in rubric.keywords_by_rule.get("R07", set()), rubric.keywords_by_rule
        assert "example" not in rubric.keywords_by_rule.get("R07", set())

        # The ljg-skills bug: R07 (scope note) labeled on a missing-example-block
        # finding is SEMANTIC drift — R07 IS valid on a Skill (type-clean) but
        # its keywords {"scope","note","related"} share nothing with the
        # pattern's tokens {"example","block"}.
        findings = [
            # type drift: R09 is agents-only
            {"category": "nl_quality", "rule_id": "R09", "file": "skills/foo/SKILL.md", "penalty": -15, "pattern": "missing-example-block", "description": "should be R06 on skill"},
            # clean
            {"category": "nl_quality", "rule_id": "R06", "file": "skills/foo/SKILL.md", "penalty": -10, "pattern": "missing-example-block", "description": "correct mapping"},
            # clean
            {"category": "nl_quality", "rule_id": "R04", "file": "skills/foo/SKILL.md", "penalty": -10, "pattern": "description-length", "description": "correct"},
            # clean
            {"category": "nl_quality", "rule_id": "R11", "file": "agents/bar.md", "penalty": -3, "pattern": "unused-tool", "description": "correct"},
            # skipped
            {"category": "bug", "rule_id": "BUG-missing-frontmatter", "file": "skills/foo/SKILL.md", "penalty": None, "pattern": "missing-fm", "description": "skipped, not nl_quality"},
            # SEMANTIC drift: ljg-skills bug verbatim
            {"category": "nl_quality", "rule_id": "R07", "file": "skills/foo/SKILL.md", "penalty": -15, "pattern": "missing-example-block", "description": "R07 is scope-note, not examples"},
        ]
        sidecar = Path(td) / "fake.findings.jsonl"
        sidecar.write_text("\n".join(json.dumps(f) for f in findings))
        drifts = validate_findings(sidecar, rubric)
        assert len(drifts) == 2, f"expected 2 drifts, got {len(drifts)}"
        kinds = sorted(d.kind for d in drifts)
        assert kinds == ["semantic", "type"], f"expected one of each kind, got {kinds}"
        semantic_drift = next(d for d in drifts if d.kind == "semantic")
        assert semantic_drift.rule_id == "R07"
        assert "example" in semantic_drift.pattern_tokens
        type_drift = next(d for d in drifts if d.kind == "type")
        assert type_drift.rule_id == "R09"
        assert type_drift.file == "skills/foo/SKILL.md"
    print("self-test PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument("paths", nargs="*", help="Specific .findings.jsonl files to check (default: all under auditor/audits/)")
    parser.add_argument("--rubric", type=Path, default=DEFAULT_RUBRIC, help="Path to scoring SKILL.md")
    parser.add_argument("--self-test", action="store_true", help="Run inline self-tests and exit")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-drift output, exit code only")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    try:
        rubric = parse_rubric(args.rubric)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    if args.paths:
        targets = [Path(p) for p in args.paths]
    else:
        targets = sorted(DEFAULT_AUDITS_DIR.glob("*.findings.jsonl"))

    if not targets:
        print(f"no .findings.jsonl files found under {DEFAULT_AUDITS_DIR}", file=sys.stderr)
        return 0

    all_drifts: list[Drift] = []
    for path in targets:
        if not path.exists():
            print(f"WARN: {path} not found, skipping", file=sys.stderr)
            continue
        all_drifts.extend(validate_findings(path, rubric))

    if not all_drifts:
        print(f"OK: {len(targets)} findings file(s) scanned, no rule_id drift detected.")
        return 0

    if not args.quiet:
        print(f"DRIFT: {len(all_drifts)} finding(s) with rule_ids not in the rubric for their artifact type:\n")
        for d in all_drifts:
            print(d.render())
            print()
    print(f"\nSUMMARY: {len(all_drifts)} drift(s) across {len(targets)} audit file(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
