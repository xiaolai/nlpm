"""Skill bodies must not contain Claude Code's dynamic-context shell syntax.

Claude Code runs the inline form (an exclamation mark directly before a
backtick code span) and the fenced form (a code fence opened by three
backticks plus an exclamation mark) whenever it loads a skill, including
when an agent preloads the skill through its `skills:` frontmatter.

nlpm's skills are reference material: they describe that syntax, they never
mean to run it. conventions-claude once quoted both forms literally, so
preloading it made Claude Code execute its prose as shell commands; the
fenced example failed and took the scorer agent down with it. This test
keeps the literal syntax out of every shipped SKILL.md.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

INLINE = re.compile(r"!`")
FENCED = re.compile(r"```!")


class SkillPreloadSafetyTest(unittest.TestCase):
    def test_no_skill_contains_dynamic_shell_syntax(self) -> None:
        skills = sorted(REPO_ROOT.glob("skills/**/SKILL.md")) + sorted(
            REPO_ROOT.glob("codex/skills/**/SKILL.md")
        )
        self.assertGreater(len(skills), 20, "skill discovery found too few files")
        offenders = []
        for path in skills:
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if INLINE.search(line) or FENCED.search(line):
                    offenders.append(f"{path.relative_to(REPO_ROOT)}:{line_no}")
        self.assertEqual(
            offenders, [],
            "these lines would run as shell commands when Claude Code loads the "
            "skill; describe the syntax in words instead:\n  " + "\n  ".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
