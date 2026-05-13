#!/usr/bin/env python3
"""validate-rule-ids.py — catch scorer drift between rubric and findings.

Parses `skills/nlpm/scoring/SKILL.md` for the per-artifact-type rule_id
catalog, then walks `auditor/audits/*.findings.jsonl` (or a path on argv)
and reports every NL-quality finding whose `rule_id` is not documented in
the rubric for that artifact's path category.

Catches TYPE drift only — rule_id valid for artifact type? It does NOT
yet check SEMANTIC drift — does the rule_id match the finding's pattern
and penalty? Example: R07 on a skill is type-valid (R07 IS in the Skills
rubric), but if the finding's pattern is "missing-example-block" with
penalty -15, the rule_id is semantically wrong (R07 is scope-note at -3;
example-block on skills is R06 at -10). Catching semantic drift requires
building a keyword-to-rule map from the rubric's Check column — tracked
as a TODO; the scorer prompt fix in auditor/prompts/score-artifacts.md
addresses semantic drift going forward.

The 2026-05-13 baseline was 861 type-drifts across 127 historical
sidecars — most are real misuses like R11 on commands (R11 is
agents-only) or R14 on skills (commands-only). The 2026-05-13
lijigang/ljg-skills R07/-15 ladder is semantic drift and is NOT
caught by the type check — only the scorer prompt fix prevents it.

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
DEFAULT_AUDITS_DIR = REPO_ROOT / "auditor" / "audits"

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
    """Allowed rule_ids per artifact type, parsed from scoring/SKILL.md."""
    by_type: dict[str, set[str]] = field(default_factory=dict)
    all_rnumbers: set[str] = field(default_factory=set)

    def allowed_for_path(self, path: str) -> set[str]:
        """Return the rubric rule_ids valid for the artifact at this path."""
        artifact_type = classify_path(path)
        return self.by_type.get(artifact_type, set())


def parse_rubric(rubric_path: Path) -> Rubric:
    """Extract rule_ids per artifact type from the rubric markdown."""
    if not rubric_path.exists():
        raise FileNotFoundError(f"rubric not found: {rubric_path}")
    text = rubric_path.read_text()
    rubric = Rubric()

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
    """A single finding whose rule_id doesn't match the rubric."""
    audit_file: str
    line_no: int
    file: str
    rule_id: str
    penalty: int | None
    pattern: str
    expected_for_type: set[str]
    artifact_type: str
    description: str

    def render(self) -> str:
        allowed_list = ", ".join(sorted(self.expected_for_type)) or "(none)"
        return (
            f"{self.audit_file}:{self.line_no}  "
            f"{self.file}\n"
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
| R09 | `<example>` blocks | Zero examples | -15 |
| R11 | Tools | Unused | -3 |
"""
    with tempfile.TemporaryDirectory() as td:
        rubric_path = Path(td) / "rubric.md"
        rubric_path.write_text(fake_rubric)
        rubric = parse_rubric(rubric_path)
        assert rubric.by_type["Skills"] == {"R04", "R06", "R07"}, rubric.by_type
        assert rubric.by_type["Agents"] == {"R09", "R11"}, rubric.by_type

        # The ljg-skills bug: R07 + -15 on a skill for missing example block
        # should be detected as drift (R07 is in the Skills rubric, but the
        # validator can't catch penalty mismatches by itself — only id-vs-type
        # is checkable structurally). However, an R09 on a skill IS catchable.
        findings = [
            {"category": "nl_quality", "rule_id": "R09", "file": "skills/foo/SKILL.md", "penalty": -15, "pattern": "missing-example-block", "description": "should be R06 on skill"},
            {"category": "nl_quality", "rule_id": "R06", "file": "skills/foo/SKILL.md", "penalty": -10, "pattern": "missing-example-block", "description": "correct mapping"},
            {"category": "nl_quality", "rule_id": "R04", "file": "skills/foo/SKILL.md", "penalty": -10, "pattern": "description-length", "description": "correct"},
            {"category": "nl_quality", "rule_id": "R11", "file": "agents/bar.md", "penalty": -3, "pattern": "unused-tool", "description": "correct"},
            {"category": "bug", "rule_id": "BUG-missing-frontmatter", "file": "skills/foo/SKILL.md", "penalty": None, "pattern": "missing-fm", "description": "skipped, not nl_quality"},
        ]
        sidecar = Path(td) / "fake.findings.jsonl"
        sidecar.write_text("\n".join(json.dumps(f) for f in findings))
        drifts = validate_findings(sidecar, rubric)
        assert len(drifts) == 1, f"expected 1 drift, got {len(drifts)}"
        assert drifts[0].rule_id == "R09", drifts[0].rule_id
        assert drifts[0].file == "skills/foo/SKILL.md", drifts[0].file
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
