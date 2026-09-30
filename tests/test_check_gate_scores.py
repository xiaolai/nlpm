"""Tests for auditor/scripts/check-gate-scores.py.

The pre-release gate asks an LLM to score every changed NL artifact and write
/tmp/scores.tsv. Twice in a row (the 1.3.1 and 1.4.0 release PRs) the model
wrote 100 for every file after reading almost none of them, and the old
assertion — "no score below 95" — passed it. This checker makes a row cost a
read: each row must quote a line that really is in the file, every listed file
must be scored exactly once, and anything malformed fails closed.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "auditor" / "scripts" / "check-gate-scores.py"

BODY_A = "---\nname: a\n---\n\nRead the config file before changing any lane.\n"
BODY_B = "---\nname: b\n---\n\nStop at the first gate failure and report the evidence.\n"


class GateScores(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "commands").mkdir()
        (self.root / "commands" / "a.md").write_text(BODY_A)
        (self.root / "commands" / "b.md").write_text(BODY_B)
        self.list = self.root / "list.txt"
        self.list.write_text("commands/a.md\ncommands/b.md\n")
        self.scores = self.root / "scores.tsv"

    def tearDown(self):
        self.tmp.cleanup()

    def run_checker(self, rows, header="file\tscore\tquote"):
        self.scores.write_text("\n".join([header, *rows]) + "\n")
        return subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(self.root), "--list", str(self.list),
             "--scores", str(self.scores), "--min", "95"],
            capture_output=True, text=True,
        )

    def good_rows(self):
        return [
            "commands/a.md\t100\tRead the config file before changing any lane.",
            "commands/b.md\t97\tStop at the first gate failure and report the evidence.",
        ]

    def test_valid_scores_pass(self):
        r = self.run_checker(self.good_rows())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("2 of 2", r.stdout)

    def test_score_below_minimum_fails(self):
        rows = self.good_rows()
        rows[1] = rows[1].replace("\t97\t", "\t90\t")
        r = self.run_checker(rows)
        self.assertEqual(r.returncode, 1)
        self.assertIn("score=90", r.stdout)

    def test_quote_not_in_file_fails(self):
        rows = self.good_rows()
        rows[0] = "commands/a.md\t100\tThis sentence appears nowhere in the file at all."
        r = self.run_checker(rows)
        self.assertEqual(r.returncode, 1)
        self.assertIn("not found in the file", r.stdout)

    def test_short_quote_fails(self):
        rows = self.good_rows()
        rows[0] = "commands/a.md\t100\tRead"
        r = self.run_checker(rows)
        self.assertEqual(r.returncode, 1)
        self.assertIn("at least", r.stdout)

    def test_frontmatter_quote_fails(self):
        rows = self.good_rows()
        rows[0] = "commands/a.md\t100\tname: a"
        r = self.run_checker(rows)
        self.assertEqual(r.returncode, 1)

    def test_missing_file_row_fails(self):
        r = self.run_checker(self.good_rows()[:1])
        self.assertEqual(r.returncode, 1)
        self.assertIn("commands/b.md", r.stdout)
        self.assertIn("not scored", r.stdout)

    def test_duplicate_row_fails(self):
        rows = self.good_rows() + [self.good_rows()[0]]
        r = self.run_checker(rows)
        self.assertEqual(r.returncode, 1)
        self.assertIn("more than once", r.stdout)

    def test_unlisted_file_fails(self):
        (self.root / "commands" / "c.md").write_text(BODY_A)
        rows = self.good_rows() + ["commands/c.md\t100\tRead the config file before changing any lane."]
        r = self.run_checker(rows)
        self.assertEqual(r.returncode, 1)
        self.assertIn("not in the list", r.stdout)

    def test_non_integer_score_fails(self):
        rows = self.good_rows()
        rows[0] = rows[0].replace("\t100\t", "\t\t")
        r = self.run_checker(rows)
        self.assertEqual(r.returncode, 1)
        self.assertIn("integer", r.stdout)

    def test_old_two_column_format_fails(self):
        r = self.run_checker(["commands/a.md\t100", "commands/b.md\t100"], header="file\tscore")
        self.assertEqual(r.returncode, 1)
        self.assertIn("header", r.stdout)

    def test_missing_scores_file_fails(self):
        r = subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(self.root), "--list", str(self.list),
             "--scores", str(self.root / "absent.tsv"), "--min", "95"],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
