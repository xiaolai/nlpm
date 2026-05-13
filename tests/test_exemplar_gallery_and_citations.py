"""Tests for the v0.8.18 exemplar gallery + citation proposer scripts.

Covers:

1. `build-exemplar-gallery.py` — frontmatter parser, deterministic
   rendering, by-score/by-rule/by-repo views, empty-input handling,
   --check freshness gate.
2. `propose-rule-citations.py` — insertion of new citation blocks,
   idempotent re-runs, replacement when exemplar set changes, removal
   when a rule loses all exemplars, --check exit codes.
3. The exemplar workflow regenerates the gallery (verified by
   substring match on the YAML).
4. The cite-exemplars workflow exists and references the right label.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GALLERY_SCRIPT = REPO_ROOT / "auditor" / "scripts" / "build-exemplar-gallery.py"
CITATIONS_SCRIPT = REPO_ROOT / "auditor" / "scripts" / "propose-rule-citations.py"
EXEMPLAR_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "auditor-exemplar.yml"
CITE_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "auditor-cite-exemplars.yml"


def _load_module(name: str, path: Path):
    """Load hyphen-named module. Must register in sys.modules BEFORE
    exec_module so @dataclass can resolve cls.__module__ on Python 3.14."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, f"could not load {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class GalleryScriptSelfTest(unittest.TestCase):
    def test_self_test_passes(self):
        result = subprocess.run(
            [sys.executable, str(GALLERY_SCRIPT), "--self-test"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
        self.assertIn("self-test PASS", result.stdout)


class GalleryFrontmatterParser(unittest.TestCase):
    def setUp(self):
        self.mod = _load_module("gallery_mod", GALLERY_SCRIPT)

    def test_full_frontmatter(self):
        result = self.mod.parse_frontmatter("""---
slug: foo-bar
repo: foo/bar
audited: 2026-05-14
commit_sha: abc1234
score: 92
exemplifies:
  - R04
  - R05
---
body
""")
        self.assertEqual(result["slug"], "foo-bar")
        self.assertEqual(result["repo"], "foo/bar")
        self.assertEqual(result["score"], "92")
        self.assertEqual(result["exemplifies"], ["R04", "R05"])

    def test_no_frontmatter(self):
        self.assertEqual(self.mod.parse_frontmatter("just a body"), {})

    def test_empty_exemplifies(self):
        result = self.mod.parse_frontmatter("""---
slug: foo
repo: foo/bar
---
""")
        self.assertEqual(result.get("exemplifies"), [])


class GalleryRendering(unittest.TestCase):
    def setUp(self):
        self.mod = _load_module("gallery_mod", GALLERY_SCRIPT)

    def test_empty_gallery(self):
        out = self.mod.render_gallery([])
        self.assertIn("No exemplars yet", out)
        self.assertTrue(out.startswith("# NLPM Exemplar Gallery"))

    def test_determinism(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            for slug, score, rules in [("a-foo", 90, ["R04"]), ("b-bar", 95, ["R04", "R06"])]:
                (d / f"{slug}.md").write_text(f"""---
slug: {slug}
repo: x/{slug}
audited: 2026-05-14
score: {score}
exemplifies:
{chr(10).join(f"  - {r}" for r in rules)}
---
""")
            exemplars = self.mod.load_exemplars(d)
            self.assertEqual(self.mod.render_gallery(exemplars),
                             self.mod.render_gallery(exemplars))

    def test_score_ordering_descending(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            for slug, score in [("a", 80), ("b", 95), ("c", 88)]:
                (d / f"{slug}.md").write_text(f"""---
slug: {slug}
repo: x/{slug}
audited: 2026-05-14
score: {score}
exemplifies:
  - R04
---
""")
            exemplars = self.mod.load_exemplars(d)
            out = self.mod.render_gallery(exemplars)
            # In the "By score" block, 95 must appear before 88 before 80
            score_section = out.split("## By score")[1].split("## By rule")[0]
            self.assertLess(score_section.find("| 95 |"), score_section.find("| 88 |"))
            self.assertLess(score_section.find("| 88 |"), score_section.find("| 80 |"))


class CitationsSelfTest(unittest.TestCase):
    def test_self_test_passes(self):
        result = subprocess.run(
            [sys.executable, str(CITATIONS_SCRIPT), "--self-test"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
        self.assertIn("self-test PASS", result.stdout)


class CitationsEditor(unittest.TestCase):
    """The edit_rules_text logic — insert, replace, remove, idempotent."""

    def setUp(self):
        self.mod = _load_module("citations_mod", CITATIONS_SCRIPT)
        self.sample = (
            "# Rules\n\n"
            "**R04. Description is a trigger.** Body.\n\n"
            "**R05. Under 500 lines.** Body.\n\n"
            "**R06. Code examples must be runnable.** Body.\n\n"
            "---\n"
        )

    def test_insert(self):
        by_rule = {"R04": [("foo", "foo.md")]}
        out = self.mod.edit_rules_text(self.sample, by_rule)
        self.assertIn(self.mod.CITATION_BEGIN, out)
        self.assertIn("[foo]", out)
        # The block must land in the R04 section, not R05 or R06
        r04_to_r05 = out.split("**R04.")[1].split("**R05.")[0]
        self.assertIn(self.mod.CITATION_BEGIN, r04_to_r05)
        r05_to_r06 = out.split("**R05.")[1].split("**R06.")[0]
        self.assertNotIn(self.mod.CITATION_BEGIN, r05_to_r06)

    def test_idempotent(self):
        by_rule = {"R04": [("foo", "foo.md")], "R06": [("bar", "bar.md")]}
        once = self.mod.edit_rules_text(self.sample, by_rule)
        twice = self.mod.edit_rules_text(once, by_rule)
        self.assertEqual(once, twice)

    def test_replacement_not_stacking(self):
        first = {"R04": [("foo", "foo.md")]}
        out1 = self.mod.edit_rules_text(self.sample, first)
        second = {"R04": [("foo", "foo.md"), ("bar", "bar.md")]}
        out2 = self.mod.edit_rules_text(out1, second)
        # Still exactly one citation block for R04
        self.assertEqual(out2.count(self.mod.CITATION_BEGIN), 1)
        self.assertIn("[bar]", out2)

    def test_remove_when_no_exemplars(self):
        with_citation = self.mod.edit_rules_text(self.sample, {"R04": [("foo", "foo.md")]})
        self.assertIn(self.mod.CITATION_BEGIN, with_citation)
        # Now no exemplars at all → block must be removed
        cleaned = self.mod.edit_rules_text(with_citation, {})
        self.assertNotIn(self.mod.CITATION_BEGIN, cleaned)
        self.assertNotIn("[foo]", cleaned)

    def test_check_mode_returns_1_on_drift(self):
        """End-to-end: create a fake rules file, fake exemplars dir, run --check."""
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            rules = tdp / "rules.md"
            rules.write_text(self.sample)
            ex_dir = tdp / "exemplars"
            ex_dir.mkdir()
            (ex_dir / "foo-bar.md").write_text("""---
slug: foo-bar
repo: foo/bar
exemplifies:
  - R04
---
""")
            result = subprocess.run(
                [sys.executable, str(CITATIONS_SCRIPT),
                 "--rules-path", str(rules),
                 "--exemplars-dir", str(ex_dir),
                 "--check"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1, msg=f"out={result.stdout} err={result.stderr}")


class WorkflowsAndIntegration(unittest.TestCase):
    """The workflows reference the right scripts and labels."""

    def test_exemplar_workflow_invokes_gallery(self):
        self.assertTrue(EXEMPLAR_WORKFLOW.exists())
        wf = EXEMPLAR_WORKFLOW.read_text()
        self.assertIn("build-exemplar-gallery.py", wf)
        self.assertIn("auditor/exemplars/README.md", wf)

    def test_cite_workflow_label_and_script(self):
        self.assertTrue(CITE_WORKFLOW.exists())
        wf = CITE_WORKFLOW.read_text()
        self.assertIn("propose-rule-citations.py", wf)
        self.assertIn("exemplar-citation-proposal", wf)
        # Workflow must NOT auto-merge — open PR for review
        self.assertIn("gh pr create", wf)
        self.assertNotIn("gh pr merge", wf)


if __name__ == "__main__":
    unittest.main()
