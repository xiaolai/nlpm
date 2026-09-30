"""Tests for auditor/scripts/validate-rule-ids.py.

This validator catches scorer drift — when the LLM scoring an artifact
labels findings with rule_ids that don't match the rubric. The 2026-05-13
lijigang/ljg-skills audit applied `rule_id: R07` + `penalty: -15` 14 times
for missing example blocks on skills, but R07 in the rubric is "scope
note" (−3); −15 is the AGENTS R09 penalty. The validator now flags this.

We test:
1. self-test passes (inline test of the parser + drift detection)
2. Rubric parser handles the real scoring SKILL.md
3. The known historical drift (R08 mislabeled as scope-note) is detected
   in the lijigang/ljg-skills sidecar — protects against the fix being
   inadvertently reverted.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "auditor" / "scripts" / "validate-rule-ids.py"
RUBRIC = REPO_ROOT / "skills" / "nlpm" / "scoring" / "SKILL.md"


def _load_validator_module():
    """Load validate-rule-ids.py as a module (filename has a hyphen).

    Must register in sys.modules BEFORE exec_module so @dataclass can resolve
    the module via cls.__module__ — without this, Python 3.14 dataclasses
    raise AttributeError on NoneType.
    """
    if "validate_rule_ids" in sys.modules:
        return sys.modules["validate_rule_ids"]
    spec = importlib.util.spec_from_file_location("validate_rule_ids", VALIDATOR)
    assert spec and spec.loader, f"could not load {VALIDATOR}"
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_rule_ids"] = module
    spec.loader.exec_module(module)
    return module


class ValidatorSelfTest(unittest.TestCase):
    """The validator ships its own --self-test; this lifts it into unittest."""

    def test_self_test_passes(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--self-test"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
        self.assertIn("self-test PASS", result.stdout)


class RubricParser(unittest.TestCase):
    """Real-rubric smoke test: the parser must recognize all artifact types."""

    def setUp(self):
        self.mod = _load_validator_module()

    def test_real_rubric_parses(self):
        rubric = self.mod.parse_rubric(RUBRIC)
        # Skills section MUST contain at least R04-R07 from the rubric tables
        self.assertIn("Skills", rubric.by_type)
        skills_rules = rubric.by_type["Skills"]
        for required in ("R04", "R05", "R06", "R07"):
            self.assertIn(required, skills_rules, f"{required} missing from Skills rubric")

    def test_agents_section_parses(self):
        rubric = self.mod.parse_rubric(RUBRIC)
        self.assertIn("Agents", rubric.by_type)
        for required in ("R09", "R10", "R11", "R12"):
            self.assertIn(required, rubric.by_type["Agents"], f"{required} missing from Agents rubric")

    def test_r06_now_covers_skill_example_blocks(self):
        """Regression: the 2026-05-13 ljg-skills fix added an R06 row for skills."""
        rubric_text = RUBRIC.read_text()
        self.assertIn(
            "Zero `<example>` blocks on a user-invocable skill (`user-invocable` absent or `true`)",
            rubric_text,
            msg="R06 example-block rule for skills must be in the Skills rubric; "
                "this fix prevents the ljg-skills R07/-15 mislabel from regressing.",
        )

    def test_r09_one_example_is_full_credit(self):
        """R09 (1.4.0): one example is full credit; exclusion and length rows exist."""
        rubric_text = RUBRIC.read_text()
        self.assertNotIn("Exactly 1 example", rubric_text)
        for row in (
            "| R09 | `<example>` blocks | Zero `<example>` blocks in the description | -15 |",
            "| R09 | Exclusion clause | Description names no situation the agent is not for",
            "| R09 | Description length | Description value over 1,200 characters, examples included | -5 |",
        ):
            self.assertIn(row, rubric_text)

    def test_codex_scoring_mirror_matches_rubric_tables(self):
        """The Codex scoring mirror must carry the same penalty tables as the Claude original."""
        codex = RUBRIC.parents[3] / "codex" / "skills" / "scoring" / "SKILL.md"
        body = lambda p: p.read_text().split("\n---\n", 1)[1]
        self.assertEqual(body(RUBRIC), body(codex))

    def test_r04_now_covers_description_length(self):
        """Regression: description-length penalty must exist under R04 for skills."""
        rubric_text = RUBRIC.read_text()
        self.assertIn("Description 500–800 chars", rubric_text)
        self.assertIn("Description >800 chars", rubric_text)


class ClassifyPath(unittest.TestCase):
    """Unit tests for the path-to-artifact-type classifier."""

    def setUp(self):
        self.mod = _load_validator_module()
        self.classify = self.mod.classify_path

    def test_skill_paths(self):
        self.assertEqual(self.classify("skills/foo/SKILL.md"), "Skills")
        self.assertEqual(self.classify(".claude/skills/foo/SKILL.md"), "Skills")

    def test_agent_paths(self):
        self.assertEqual(self.classify("agents/foo.md"), "Agents")
        self.assertEqual(self.classify(".claude/agents/foo.md"), "Agents")

    def test_command_paths(self):
        self.assertEqual(self.classify("commands/foo.md"), "Commands")

    def test_manifests(self):
        self.assertEqual(self.classify(".claude-plugin/plugin.json"), "plugin.json")
        self.assertEqual(self.classify(".mcp.json"), ".mcp.json")

    def test_default_falls_to_skills(self):
        """Unknown paths fall to Skills (most NL artifacts are skills)."""
        self.assertEqual(self.classify("docs/random.md"), "Skills")


class SemanticDrift(unittest.TestCase):
    """The v0.8.16 semantic check: rule_id ↔ pattern keyword alignment."""

    def setUp(self):
        self.mod = _load_validator_module()
        self.rubric = self.mod.parse_rubric(RUBRIC)

    def test_r07_with_example_pattern_is_semantic_drift(self):
        """R07 (scope note) on a skill is type-valid but semantic drift when
        the pattern is missing-example-block. This is the ljg-skills bug."""
        with tempfile.TemporaryDirectory() as td:
            sidecar = Path(td) / "fake.findings.jsonl"
            sidecar.write_text(json.dumps({
                "category": "nl_quality",
                "rule_id": "R07",
                "file": "skills/foo/SKILL.md",
                "penalty": -15,
                "pattern": "missing-example-block",
                "description": "R07 is scope-note, not examples",
            }))
            drifts = self.mod.validate_findings(sidecar, self.rubric)
            self.assertEqual(len(drifts), 1)
            self.assertEqual(drifts[0].kind, "semantic")
            self.assertEqual(drifts[0].rule_id, "R07")
            self.assertIn("scope", drifts[0].rule_keywords)
            self.assertIn("example", drifts[0].pattern_tokens)
            self.assertFalse(drifts[0].rule_keywords & drifts[0].pattern_tokens)

    def test_r07_with_scope_note_pattern_is_clean(self):
        """R07 with a pattern that mentions 'scope' or 'note' should pass."""
        with tempfile.TemporaryDirectory() as td:
            sidecar = Path(td) / "fake.findings.jsonl"
            sidecar.write_text(json.dumps({
                "category": "nl_quality",
                "rule_id": "R07",
                "file": "skills/foo/SKILL.md",
                "penalty": -3,
                "pattern": "no_scope_note",
                "description": "correct scope-note use",
            }))
            self.assertEqual(self.mod.validate_findings(sidecar, self.rubric), [])

    def test_singularization_lets_examples_match_example(self):
        """Plural in rule title vs singular in pattern token must still match."""
        tokenize = self.mod._tokenize
        # R06's title is "Code examples must be runnable." → contains "examples" → "example"
        self.assertIn("example", tokenize("Code examples must be runnable"))
        self.assertIn("example", tokenize("missing-example-block"))


class DriftDetection(unittest.TestCase):
    """Stage the known ljg-skills bug pattern and confirm the validator catches it."""

    def setUp(self):
        self.mod = _load_validator_module()

    def test_r09_on_skill_is_drift(self):
        """R09 (agent example rule) used on a SKILL.md = drift."""
        rubric = self.mod.parse_rubric(RUBRIC)
        with tempfile.TemporaryDirectory() as td:
            sidecar = Path(td) / "fake.findings.jsonl"
            sidecar.write_text(json.dumps({
                "category": "nl_quality",
                "rule_id": "R09",
                "file": "skills/foo/SKILL.md",
                "penalty": -15,
                "pattern": "missing-example-block",
                "description": "R09 is an agent rule, should be R06 on skills",
            }))
            drifts = self.mod.validate_findings(sidecar, rubric)
            self.assertEqual(len(drifts), 1)
            self.assertEqual(drifts[0].rule_id, "R09")
            self.assertEqual(drifts[0].artifact_type, "Skills")

    def test_r06_on_skill_is_clean(self):
        """R06 (the corrected skill example-block rule) is clean."""
        rubric = self.mod.parse_rubric(RUBRIC)
        with tempfile.TemporaryDirectory() as td:
            sidecar = Path(td) / "fake.findings.jsonl"
            sidecar.write_text(json.dumps({
                "category": "nl_quality",
                "rule_id": "R06",
                "file": "skills/foo/SKILL.md",
                "penalty": -10,
                "pattern": "missing-example-block",
                "description": "correct R06 mapping",
            }))
            self.assertEqual(self.mod.validate_findings(sidecar, rubric), [])

    def test_universal_rules_dont_drift_anywhere(self):
        """R01–R03 are universal — valid on any artifact type."""
        rubric = self.mod.parse_rubric(RUBRIC)
        with tempfile.TemporaryDirectory() as td:
            sidecar = Path(td) / "fake.findings.jsonl"
            sidecar.write_text(json.dumps({
                "category": "nl_quality",
                "rule_id": "R01",
                "file": "agents/bar.md",
                "penalty": -2,
                "pattern": "vague-quantifier",
                "description": "R01 is universal, should NOT drift",
            }))
            self.assertEqual(self.mod.validate_findings(sidecar, rubric), [])

    def test_bug_and_cc_categories_are_skipped(self):
        """BUG-* and CC-* prefixes aren't R-numbered quality rules."""
        rubric = self.mod.parse_rubric(RUBRIC)
        with tempfile.TemporaryDirectory() as td:
            sidecar = Path(td) / "fake.findings.jsonl"
            sidecar.write_text("\n".join(json.dumps(f) for f in [
                {"category": "bug", "rule_id": "BUG-missing-frontmatter", "file": "skills/x/SKILL.md", "penalty": None, "pattern": "x", "description": "x"},
                {"category": "cross_component", "rule_id": "CC-stale-count", "file": "CLAUDE.md", "penalty": None, "pattern": "x", "description": "x"},
            ]))
            self.assertEqual(self.mod.validate_findings(sidecar, rubric), [])


if __name__ == "__main__":
    unittest.main()
