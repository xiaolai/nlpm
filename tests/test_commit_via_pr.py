"""Tests for the auditor's bot-commit path under concurrency.

Every auditor workflow lands its output through
auditor/scripts/commit-via-pr.sh; concurrent runs (the Audit Repo batch
dispatches ~5 at the same minute) race on the shared files, and the loser
rebases through auditor/scripts/resolve-merge-conflicts.sh. These tests
drive the real scripts against real git repositories.

Properties under test:

* The resolver keeps THIS commit's version during a rebase — the mode every
  caller uses — not upstream's. Git's `:2`/`--ours` means upstream during a
  rebase; the resolver used to assume the merge mapping and silently
  discarded the bot's registry fields and files.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "auditor" / "scripts"

FAKE_REPO = "example/nlpm"
FAKE_TOKEN = "test-token"

def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=check, capture_output=True, text=True
    )


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def registry(repos: dict) -> str:
    return json.dumps({"repos": repos}, indent=2) + "\n"


class GitSandbox(unittest.TestCase):
    """A bare `origin` seeded with the auditor scripts and shared files."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="nlpm-commit-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.origin = self.tmp / "origin.git"
        git(self.tmp, "init", "--bare", "-b", "main", str(self.origin))

        seed = self.tmp / "seed"
        git(self.tmp, "clone", "-q", str(self.origin), str(seed))
        self._identity(seed)
        shutil.copytree(SCRIPTS, seed / "auditor" / "scripts")
        write(seed / "auditor/registry/repos.json", registry({
            "a/x": {"status": "discovered", "score": None},
            "b/y": {"status": "audited", "score": 70},
        }))
        write(seed / "auditor/logs/events.jsonl", '{"e":0}\n')
        write(seed / "auditor/findings.jsonl", '{"f":0}\n')
        write(seed / "auditor/audits/shared.md", "base\n")
        git(seed, "add", "-A")
        git(seed, "commit", "-q", "-m", "seed")
        git(seed, "push", "-q", "origin", "main")

    @staticmethod
    def _identity(repo: Path) -> None:
        git(repo, "config", "user.name", "test")
        git(repo, "config", "user.email", "test@example.com")
        git(repo, "config", "commit.gpgsign", "false")
        # Hermetic: never run the host's global hooks inside the sandbox.
        git(repo, "config", "core.hooksPath", os.devnull)

    def clone(self, name: str) -> Path:
        path = self.tmp / name
        git(self.tmp, "clone", "-q", str(self.origin), str(path))
        self._identity(path)
        # commit-via-pr.sh rewrites origin to the GitHub HTTPS URL; route it
        # back to the local bare repo.
        git(path, "config",
            f"url.{self.origin}.insteadOf",
            f"https://x-access-token:{FAKE_TOKEN}@github.com/{FAKE_REPO}.git")
        return path

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text())


class ResolverKeepsThisCommit(GitSandbox):
    """resolve-merge-conflicts.sh: two concurrent commits to the shared files."""

    def _race(self, integrate: list[str]) -> Path:
        sibling = self.clone("sibling")
        bot = self.clone("bot")

        # The sibling run lands first.
        reg = self.read_json(sibling / "auditor/registry/repos.json")
        reg["repos"]["a/x"]["status"] = "tracked"
        reg["repos"]["b/y"]["score"] = 75
        write(sibling / "auditor/registry/repos.json", registry(reg["repos"]))
        write(sibling / "auditor/logs/events.jsonl", '{"e":0}\n{"e":"sibling"}\n')
        write(sibling / "auditor/findings.jsonl", '{"f":0}\n{"f":"sibling"}\n')
        write(sibling / "auditor/audits/shared.md", "sibling\n")
        git(sibling, "commit", "-q", "-am", "sibling")
        git(sibling, "push", "-q", "origin", "main")

        # This run committed against the old main.
        reg = self.read_json(bot / "auditor/registry/repos.json")
        reg["repos"]["a/x"]["status"] = "audited"
        reg["repos"]["c/z"] = {"status": "audited", "score": 90}
        write(bot / "auditor/registry/repos.json", registry(reg["repos"]))
        write(bot / "auditor/logs/events.jsonl", '{"e":0}\n{"e":"bot"}\n')
        write(bot / "auditor/findings.jsonl", '{"f":0}\n{"f":"bot"}\n')
        write(bot / "auditor/audits/shared.md", "bot\n")
        git(bot, "commit", "-q", "-am", "bot")

        git(bot, "fetch", "-q", "origin", "main")
        conflicted = git(bot, *integrate, "origin/main", check=False)
        self.assertNotEqual(conflicted.returncode, 0, "the race must produce a conflict")
        resolved = subprocess.run(
            ["bash", "auditor/scripts/resolve-merge-conflicts.sh"],
            cwd=bot, capture_output=True, text=True,
        )
        self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
        env = {**os.environ, "GIT_EDITOR": "true"}
        cont = "rebase" if integrate[0] == "rebase" else "commit"
        args = ["--continue"] if cont == "rebase" else ["--no-edit"]
        subprocess.run(["git", cont, *args], cwd=bot, env=env, check=True,
                       capture_output=True)
        self.assertEqual(git(bot, "diff", "--name-only", "--diff-filter=U").stdout, "")
        return bot

    def _assert_bot_work_survives(self, bot: Path) -> None:
        repos = self.read_json(bot / "auditor/registry/repos.json")["repos"]
        self.assertEqual(repos["a/x"]["status"], "audited",
                         "overlapping field: this commit's value must win")
        self.assertEqual(repos["b/y"]["score"], 75,
                         "field only upstream changed must keep upstream's value")
        self.assertEqual(repos["c/z"], {"status": "audited", "score": 90},
                         "entry only this commit added must survive")
        self.assertEqual(
            (bot / "auditor/logs/events.jsonl").read_text(),
            '{"e":0}\n{"e":"sibling"}\n{"e":"bot"}\n',
            "append-only log: upstream lines first, then this commit's, none lost",
        )
        self.assertEqual(
            (bot / "auditor/findings.jsonl").read_text(),
            '{"f":0}\n{"f":"sibling"}\n{"f":"bot"}\n',
        )
        self.assertEqual((bot / "auditor/audits/shared.md").read_text(), "bot\n",
                         "other files: this commit's version, never a silent revert")

    def test_rebase_keeps_this_commits_work(self) -> None:
        self._assert_bot_work_survives(self._race(["rebase"]))

    def test_merge_keeps_this_commits_work(self) -> None:
        self._assert_bot_work_survives(self._race(["merge", "--no-edit"]))


if __name__ == "__main__":
    unittest.main()
