"""Skill bodies must survive being loaded by Claude Code unchanged.

Claude Code rewrites a skill's text whenever it loads it, including when an
agent preloads the skill through its `skills:` frontmatter. nlpm's skills are
reference material: they describe that machinery, they never mean to trigger
it. Two kinds of rewrite are guarded here.

1. Dynamic-context shell syntax. Claude Code runs the inline form (an
   exclamation mark directly before a backtick code span) and the fenced form
   (a code fence opened by three backticks plus an exclamation mark).
   conventions-claude once quoted both forms literally, so preloading it made
   Claude Code execute its prose as shell commands; the fenced example failed
   and took the scorer agent down with it.

2. String substitution. Claude Code replaces the all-arguments token (a dollar
   sign followed by ARGUMENTS) with the invocation's arguments, and every
   dollar-brace CLAUDE_* variable with its value. On a preload the arguments
   are empty, so conventions-claude section 2.4, the list of variable names the
   scorer must not flag, reached the scorer as an empty string, a session ID
   and a few absolute paths. Observed on Claude Code 2.1.285 by preloading a
   probe skill and reading the subagent transcript; a backslash protected the
   arguments token but not the braced variables. The skills therefore write
   these tokens split by a `+`, which no substitution matches.

Both checks cover every shipped SKILL.md, Claude and Codex trees alike: a
skill loaded through the Skill tool is rewritten the same way, and the Codex
mirrors must state the same text as their sources.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

INLINE = re.compile(r"!`")
FENCED = re.compile(r"```!")

# Tokens Claude Code substituted when an agent preloaded a skill (2.1.285).
# user_config is substituted only for plugins that declare userConfig; it is
# guarded too so that adding userConfig later cannot silently garble a skill.
SUBSTITUTED = re.compile(r"\$ARGUMENTS|\$\{CLAUDE_[A-Z_]+\}|\$\{user_config\.")

# `skills:` block list in agent frontmatter, e.g. "  - nlpm:conventions".
PRELOAD_ENTRY = re.compile(r"^\s*-\s*nlpm:([a-z0-9-]+)\s*$")


def shipped_skills() -> list[Path]:
    return sorted(REPO_ROOT.glob("skills/**/SKILL.md")) + sorted(
        REPO_ROOT.glob("codex/skills/**/SKILL.md")
    )


def offending_lines(pattern: re.Pattern[str]) -> list[str]:
    offenders = []
    for path in shipped_skills():
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if pattern.search(line):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{line_no}")
    return offenders


def preloaded_skill_names() -> set[str]:
    """Skill names listed under `skills:` in any agent's frontmatter."""
    names: set[str] = set()
    for agent in sorted(REPO_ROOT.glob("agents/*.md")):
        text = agent.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not match:
            continue
        in_skills = False
        for line in match.group(1).splitlines():
            if line.startswith("skills:"):
                in_skills = True
                continue
            if in_skills:
                entry = PRELOAD_ENTRY.match(line)
                if entry:
                    names.add(entry.group(1))
                elif line and not line[0].isspace():
                    in_skills = False
    return names


class SkillPreloadSafetyTest(unittest.TestCase):
    def test_skill_discovery_finds_the_skills(self) -> None:
        self.assertGreater(len(shipped_skills()), 20, "skill discovery found too few files")

    def test_every_preloaded_skill_is_scanned(self) -> None:
        # A preloaded skill outside the scanned globs would pass every check
        # below without being read.
        preloaded = preloaded_skill_names()
        self.assertGreater(len(preloaded), 3, "found too few preloaded skills; did the agent frontmatter format change?")
        scanned = set(shipped_skills())
        missing = sorted(
            name for name in preloaded
            if (REPO_ROOT / "skills" / "nlpm" / name / "SKILL.md") not in scanned
        )
        self.assertEqual(missing, [], "agents preload skills this test does not scan: " + ", ".join(missing))

    def test_no_skill_contains_dynamic_shell_syntax(self) -> None:
        offenders = [
            line for pattern in (INLINE, FENCED) for line in offending_lines(pattern)
        ]
        self.assertEqual(
            offenders, [],
            "these lines would run as shell commands when Claude Code loads the "
            "skill; describe the syntax in words instead:\n  " + "\n  ".join(offenders),
        )

    def test_no_skill_contains_a_substituted_token(self) -> None:
        offenders = offending_lines(SUBSTITUTED)
        self.assertEqual(
            offenders, [],
            "Claude Code replaces these tokens with values when it loads or "
            "preloads the skill, so the reader never sees the token. Write it "
            "split by a `+` (e.g. `$+ARGUMENTS`, `$+{CLAUDE_PLUGIN_ROOT}`) as "
            "nlpm:conventions-claude section 2.4 does:\n  " + "\n  ".join(offenders),
        )

    def test_substitution_pattern_matches_the_observed_tokens(self) -> None:
        for token in ("$ARGUMENTS", "${CLAUDE_PLUGIN_ROOT}", "${CLAUDE_SKILL_DIR}",
                      "${CLAUDE_SESSION_ID}", "${CLAUDE_EFFORT}", "${CLAUDE_PLUGIN_DATA}",
                      "${CLAUDE_PROJECT_DIR}", "${user_config.api_key}"):
            self.assertRegex(token, SUBSTITUTED)
        for safe in ("$+ARGUMENTS", "$+{CLAUDE_PLUGIN_ROOT}", "$CLAUDE_PLUGIN_ROOT", "$1"):
            self.assertNotRegex(safe, SUBSTITUTED)


if __name__ == "__main__":
    unittest.main()
