"""Every event an auditor workflow logs must be committed.

log_event appends to auditor/logs/events.jsonl on the runner. A line appended
after a workflow's last commit (commit-via-pr.sh / git-push-with-retry.sh) is
discarded with the runner. auditor-exemplar.yml logged `exemplar_published`
after its commit, so main never held a single one of those events.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"
COMMIT = re.compile(r"commit-via-pr\.sh|git-push-with-retry\.sh")
LOG = re.compile(r"^\s*log_event\s")
# Workflows whose events are deliberately never committed.
EXEMPT = {"auditor-integration-test.yml"}  # exercises log-event.sh itself


class EventsAreCommitted(unittest.TestCase):
    def test_no_log_event_after_the_last_commit(self) -> None:
        checked = 0
        for wf in sorted(WORKFLOWS.glob("*.yml")):
            if wf.name in EXEMPT:
                continue
            lines = wf.read_text().splitlines()
            commits = [i for i, l in enumerate(lines)
                       if COMMIT.search(l) and not l.strip().startswith("#")]
            logs = [i for i, l in enumerate(lines) if LOG.match(l)]
            if not logs:
                continue
            checked += 1
            with self.subTest(workflow=wf.name):
                self.assertTrue(commits, f"{wf.name} logs events but never commits them")
                late = [i + 1 for i in logs if i > max(commits)]
                self.assertEqual(late, [], f"{wf.name}: log_event after the last commit, at lines {late}")
        self.assertGreater(checked, 0, "no workflow logs events; the pattern no longer matches")


if __name__ == "__main__":
    unittest.main()
