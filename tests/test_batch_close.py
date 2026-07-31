"""Tests for the phase-4 terminal-issue auto-close logic in batch-process.py.

Phase 4 closes an "Audit candidate" issue once its repo has reached a
terminal registry status, so the tracker reflects only live work. The
decision is a pure predicate (`_terminal_close_note`) plus a date helper
(`_issue_age_days`), both unit-testable without gh/GHA mocking.

The safety property under test: an issue is NEVER closed while its repo is
still backlog (`discovered`/`none`) or a fresh audit awaiting promotion, and
NEVER while it carries an action-pending label. Closing too early would make
the pipeline skip contributing to that repo — the asymmetric risk this phase
must avoid.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BATCH_PROCESS = REPO_ROOT / "auditor" / "scripts" / "batch-process.py"


def _load_module(name: str, path: Path):
    """Load a hyphenated-filename script as a module. See test_exemplar_helpers.py."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, f"could not load {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class TerminalCloseNote(unittest.TestCase):
    """batch-process.py: _terminal_close_note (pure close decision)."""

    def setUp(self):
        self.bp = _load_module("batch_process", BATCH_PROCESS)
        # Age comfortably past the default 3d grace for the audited cases.
        self.old = self.bp.AUDITED_CLOSE_GRACE_DAYS + 5

    def _note(self, status, labels=frozenset(), age_days=None):
        if age_days is None:
            age_days = self.old
        return self.bp._terminal_close_note(status, set(labels), age_days)

    def test_terminal_statuses_close_immediately(self):
        for status in ("contributed", "tracked", "complete", "policy_denied", "orphaned"):
            with self.subTest(status=status):
                note = self._note(status, age_days=0.0)
                self.assertIsNotNone(note)
                self.assertIn(status, note)

    def test_backlog_statuses_never_close(self):
        # discovered/none are backlog — phase1_5 owns them; must not close
        # even when very old.
        for status in ("discovered", "none", ""):
            with self.subTest(status=status):
                self.assertIsNone(self._note(status, age_days=999.0))

    def test_fresh_audited_is_protected(self):
        # A just-audited repo may still be promoted by phase1_promote.
        self.assertIsNone(self._note("audited", age_days=0.0))
        self.assertIsNone(
            self._note("audited", age_days=self.bp.AUDITED_CLOSE_GRACE_DAYS - 0.01)
        )

    def test_audited_closes_past_grace(self):
        note = self._note("audited", age_days=self.bp.AUDITED_CLOSE_GRACE_DAYS)
        self.assertIsNotNone(note)
        self.assertIn("audited", note)

    def test_action_pending_label_blocks_close(self):
        # Even a terminal status must not close while an action is queued.
        for label in ("audit-candidate", "audit-ready", "contribute-approved",
                      "case-study-ready", "security-blocked"):
            with self.subTest(label=label):
                self.assertIsNone(
                    self._note("contributed", labels={label}, age_days=self.old)
                )
                self.assertIsNone(
                    self._note("audited", labels={label}, age_days=self.old)
                )

    def test_benign_terminal_labels_do_not_block(self):
        # prs-submitted / case-study-clean / exemplar-published are not
        # action-pending — they must not veto a close.
        for label in ("prs-submitted", "case-study-clean", "exemplar-published"):
            with self.subTest(label=label):
                self.assertIsNotNone(
                    self._note("contributed", labels={label}, age_days=self.old)
                )


class IssueAgeDays(unittest.TestCase):
    """batch-process.py: _issue_age_days (parse failures must read as fresh)."""

    def setUp(self):
        self.bp = _load_module("batch_process", BATCH_PROCESS)

    def test_missing_or_empty_is_zero(self):
        # Fresh (0.0), so the grace guard does NOT close on a missing stamp.
        self.assertEqual(self.bp._issue_age_days(None), 0.0)
        self.assertEqual(self.bp._issue_age_days(""), 0.0)

    def test_malformed_is_zero(self):
        self.assertEqual(self.bp._issue_age_days("not-a-date"), 0.0)

    def test_old_timestamp_is_positive_and_large(self):
        # A 2020 timestamp is many years old → well past any grace window.
        self.assertGreater(self.bp._issue_age_days("2020-01-01T00:00:00Z"), 365.0)


if __name__ == "__main__":
    unittest.main()
