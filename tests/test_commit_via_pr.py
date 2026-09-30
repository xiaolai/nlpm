"""Tests for the auditor's bot-commit path under concurrency.

Every auditor workflow lands its output through
auditor/scripts/commit-via-pr.sh; concurrent runs (the Audit Repo batch
dispatches ~5 at the same minute) race on the shared files, and the loser
rebases through auditor/scripts/resolve-merge-conflicts.sh. These tests
drive the real scripts against real git repositories, with a fake `gh` on
PATH standing in for GitHub.

Properties under test:

* The resolver keeps THIS commit's version during a rebase — the mode every
  caller uses — not upstream's. Git's `:2`/`--ours` means upstream during a
  rebase; the resolver used to assume the merge mapping and silently
  discarded the bot's registry fields and files.
* A job may call commit-via-pr.sh twice (audit, then disclosure-pending)
  while the first PR is still open, without dying on `gh pr create`
  (run 36677482481).
* With auto-merge disabled on the repo, the watch loop keeps retrying a
  direct merge instead of leaving the PR open forever.
* The janitor merges young CLEAN bot PRs and leaves old ones for a human.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "auditor" / "scripts"

FAKE_REPO = "example/nlpm"
FAKE_TOKEN = "test-token"

# A stand-in for the gh CLI. State lives in $FAKE_GH_STATE (JSON); every
# call is appended to $FAKE_GH_LOG. Behaviour knobs:
#   FAKE_GH_DIRECT_MERGE_FAILS  number of direct merges that fail before one succeeds
#   FAKE_GH_LIST                lines printed verbatim by `gh pr list`
#   FAKE_GH_MERGE_STATES        JSON {pr number: mergeStateStatus} for `gh pr view --json mergeStateStatus`
#   FAKE_GH_CREATE_502          number of `gh pr create` calls that open the PR, then fail before labelling it
FAKE_GH = textwrap.dedent(
    r'''
    #!/usr/bin/env python3
    import json, os, sys
    args = sys.argv[1:]
    state_path = os.environ["FAKE_GH_STATE"]
    try:
        state = json.load(open(state_path))
    except FileNotFoundError:
        state = {"prs": {}, "next": 1, "direct_failures": 0}
    with open(os.environ["FAKE_GH_LOG"], "a") as log:
        log.write(json.dumps(args) + "\n")

    def save():
        json.dump(state, open(state_path, "w"))

    def opt(name):
        return args[args.index(name) + 1] if name in args else None

    if args[:2] == ["pr", "create"]:
        head = opt("--head")
        for pr in state["prs"].values():
            if pr["head"] == head and pr["state"] == "OPEN":
                sys.stderr.write(f'a pull request for branch "{head}" into branch "main" already exists:\n')
                sys.exit(1)
        num = str(state["next"])
        state["next"] += 1
        state["prs"][num] = {"head": head, "state": "OPEN", "labels": []}
        if state.get("create_502s", 0) < int(os.environ.get("FAKE_GH_CREATE_502", "0")):
            # GitHub opened the PR, then the call failed before the label was added.
            state["create_502s"] = state.get("create_502s", 0) + 1
            save()
            sys.stderr.write("pull request create failed: HTTP 502: 502 Bad Gateway\n")
            sys.exit(1)
        state["prs"][num]["labels"] = ["auditor-bot"]
        save()
        print(f"https://github.com/example/nlpm/pull/{num}")
    elif args[:2] == ["pr", "merge"]:
        if "--auto" in args:
            sys.stderr.write("GraphQL: Auto merge is not allowed for this repository\n")
            sys.exit(1)
        num = args[2].rsplit("/", 1)[-1]
        if state["direct_failures"] < int(os.environ.get("FAKE_GH_DIRECT_MERGE_FAILS", "0")):
            state["direct_failures"] += 1
            save()
            sys.stderr.write("Pull request is not mergeable\n")
            sys.exit(1)
        state["prs"].setdefault(num, {"head": "?", "state": "OPEN"})["state"] = "MERGED"
        save()
    elif args[:2] == ["pr", "view"] and "mergeStateStatus" in (opt("--json") or "") and "state" not in (opt("--json") or "").split(","):
        # Per-PR merge state, as the janitor re-queries an UNKNOWN from `gh pr list`.
        num = args[2].rsplit("/", 1)[-1]
        print(json.loads(os.environ.get("FAKE_GH_MERGE_STATES", "{}")).get(num, "UNKNOWN"))
    elif args[:2] == ["pr", "view"]:
        num = args[2].rsplit("/", 1)[-1]
        pr = state["prs"].get(num, {"state": "OPEN"})
        print(f'{pr["state"]} CLEAN')
    elif args[:2] == ["pr", "list"] and "--head" in args:
        head = opt("--head")
        for num, pr in state["prs"].items():
            if pr["head"] == head and pr["state"] == "OPEN":
                print(f"https://github.com/example/nlpm/pull/{num}")
                break
    elif args[:2] == ["pr", "list"]:
        sys.stdout.write(os.environ.get("FAKE_GH_LIST", ""))
    elif args[:2] == ["pr", "edit"]:
        num = args[2].rsplit("/", 1)[-1]
        pr = state["prs"].setdefault(num, {"head": "?", "state": "OPEN", "labels": []})
        pr.setdefault("labels", []).append(opt("--add-label"))
        save()
    elif args[:2] == ["pr", "close"]:
        pass
    else:
        sys.stderr.write(f"fake gh: unhandled {args}\n")
        sys.exit(2)
    '''
).lstrip()


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


class FakeGhSandbox(GitSandbox):
    """A job checkout plus a fake gh (auto-merge disabled) on PATH."""

    def setUp(self) -> None:
        super().setUp()
        bindir = self.tmp / "bin"
        bindir.mkdir()
        gh = bindir / "gh"
        gh.write_text(FAKE_GH)
        gh.chmod(0o755)
        self.state = self.tmp / "gh-state.json"
        self.log = self.tmp / "gh-log.jsonl"
        self.env = {
            **os.environ,
            "PATH": f"{bindir}{os.pathsep}{os.environ['PATH']}",
            "FAKE_GH_STATE": str(self.state),
            "FAKE_GH_LOG": str(self.log),
            "GITHUB_REPOSITORY": FAKE_REPO,
            "GITHUB_WORKFLOW": "Audit Repo",
            "GITHUB_RUN_ID": "123",
            "PAT_TOKEN": FAKE_TOKEN,
            "COMMIT_VIA_PR_MAX_WATCH": "2",
            "COMMIT_VIA_PR_SHORT_SLEEP": "0",
            "COMMIT_VIA_PR_LONG_SLEEP": "0",
        }
        self.job = self.clone("job")

    def gh_calls(self) -> list[list[str]]:
        return [json.loads(line) for line in self.log.read_text().splitlines()]


class CommitViaPr(FakeGhSandbox):
    """commit-via-pr.sh against a fake gh with auto-merge disabled."""

    def commit_via_pr(self, message: str, **env: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bash", "auditor/scripts/commit-via-pr.sh", message],
            cwd=self.job, env={**self.env, **env}, capture_output=True, text=True,
        )

    def test_second_call_in_one_job_gets_its_own_pr(self) -> None:
        # Direct merges keep failing, so the first PR is still open when the
        # second call runs — the state of run 36677482481.
        stuck = {"FAKE_GH_DIRECT_MERGE_FAILS": "99"}
        write(self.job / "auditor/audits/r.md", "audit\n")
        git(self.job, "add", "-A")
        first = self.commit_via_pr("audit: r", **stuck)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)

        write(self.job / "auditor/disclosures-pending/r.md", "disclosure\n")
        git(self.job, "add", "-A")
        second = self.commit_via_pr("disclosure-pending: r", **stuck)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)

        heads = [c[c.index("--head") + 1] for c in self.gh_calls() if c[:2] == ["pr", "create"]]
        self.assertEqual(len(heads), 2)
        self.assertNotEqual(heads[0], heads[1], "each call must open its own PR branch")
        remote = git(self.origin, "for-each-ref", "--format=%(refname:short)",
                     "refs/heads/auditor/bot/").stdout.split()
        self.assertEqual(sorted(remote), sorted(heads))
        # The second branch carries both commits; nothing staged was dropped.
        files = git(self.origin, "ls-tree", "-r", "--name-only", heads[1]).stdout.split()
        self.assertIn("auditor/audits/r.md", files)
        self.assertIn("auditor/disclosures-pending/r.md", files)

    def test_half_created_pr_is_adopted_labelled_and_merged(self) -> None:
        # Write Exemplar run 36713682847: `gh pr create` returned HTTP 502 after
        # GitHub had opened the PR (#1312) but before it was labelled. The job
        # died and the unlabelled PR was invisible to the janitor.
        write(self.job / "auditor/exemplars/r.md", "exemplar\n")
        git(self.job, "add", "-A")
        result = self.commit_via_pr("exemplar: r", FAKE_GH_CREATE_502="1")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        creates = [c for c in self.gh_calls() if c[:2] == ["pr", "create"]]
        self.assertEqual(len(creates), 1, "an existing PR for the branch is adopted, not re-created")
        state = json.loads(self.state.read_text())
        self.assertEqual(len(state["prs"]), 1)
        pr = next(iter(state["prs"].values()))
        self.assertIn("auditor-bot", pr["labels"])
        self.assertEqual(pr["state"], "MERGED")

    def test_direct_merge_is_retried_when_auto_merge_is_disabled(self) -> None:
        write(self.job / "auditor/audits/r.md", "audit\n")
        git(self.job, "add", "-A")
        result = self.commit_via_pr("audit: r", FAKE_GH_DIRECT_MERGE_FAILS="1")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("commit-via-pr: merged", result.stdout)
        merges = [c for c in self.gh_calls() if c[:2] == ["pr", "merge"]]
        direct = [c for c in merges if "--auto" not in c]
        self.assertEqual(len(direct), 2, "failed direct merge must be retried in the loop")
        self.assertEqual(len(merges) - len(direct), 1,
                         "--auto is tried once, not re-asserted every tick once known unavailable")


class UnstickMergesMergeable(FakeGhSandbox):
    """unstick-bot-prs.sh merges young CLEAN bot PRs, warns about old ones."""

    def test_merges_young_clean_and_leaves_old(self) -> None:
        listing = "\n".join([
            "11 auditor/bot/a/1 CLEAN 3 1",
            "12 auditor/bot/a/2 UNSTABLE 3 1",
            "13 auditor/bot/a/3 CLEAN 1300 1",
            "14 auditor/bot/a/4 HAS_HOOKS 0 1",
        ]) + "\n"
        result = subprocess.run(
            ["bash", "auditor/scripts/unstick-bot-prs.sh"],
            cwd=self.job, env={**self.env, "FAKE_GH_LIST": listing},
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        merged = [c[2] for c in self.gh_calls() if c[:2] == ["pr", "merge"]]
        self.assertEqual(merged, ["11", "14"])
        self.assertIn("#13 (1300h)", result.stdout)
        self.assertIn("no conflicting auditor-bot PRs", result.stdout)

    def test_unlabelled_bot_pr_is_found_by_branch_and_labelled(self) -> None:
        listing = "31 auditor/bot/a/1 CLEAN 1 0\n"
        result = subprocess.run(
            ["bash", "auditor/scripts/unstick-bot-prs.sh"],
            cwd=self.job, env={**self.env, "FAKE_GH_LIST": listing},
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.gh_calls()
        self.assertIn(["pr", "edit", "31", "--repo", self.env["GITHUB_REPOSITORY"], "--add-label", "auditor-bot"], calls)
        self.assertEqual([c[2] for c in calls if c[:2] == ["pr", "merge"]], ["31"])
        lists = [c for c in calls if c[:2] == ["pr", "list"]]
        self.assertNotIn("--label", lists[0], "bot PRs are selected by branch, since the label can be missing")

    def test_listing_excludes_fork_branches(self) -> None:
        # The listing's jq filter is what keeps a fork PR named auditor/bot/…
        # from being labelled and merged. Check the filter itself with jq.
        script = (REPO_ROOT / "auditor/scripts/unstick-bot-prs.sh").read_text()
        jq_filter = script.split("--jq '", 1)[1].split("'", 1)[0]
        prs = [
            {"number": 41, "headRefName": "auditor/bot/a/1", "mergeStateStatus": "CLEAN",
             "createdAt": "2026-09-30T00:00:00Z", "labels": [], "isCrossRepository": True},
            {"number": 42, "headRefName": "auditor/bot/a/2", "mergeStateStatus": "CLEAN",
             "createdAt": "2026-09-30T00:00:00Z", "labels": [], "isCrossRepository": False},
        ]
        out = subprocess.run(["jq", "-r", jq_filter], input=json.dumps(prs),
                             capture_output=True, text=True, check=True).stdout.split()
        self.assertIn("42", out)
        self.assertNotIn("41", out, "a fork PR must never be selected, whatever its branch is called")

    def test_unknown_state_is_rechecked_per_pr(self) -> None:
        # GitHub recomputes every open PR's mergeability after main moves, and
        # `gh pr list` reports UNKNOWN until it finishes. The 2026-09-30 09:51
        # sweep, ten minutes after a merge to main, saw four CLEAN bot PRs as
        # UNKNOWN and merged none of them.
        listing = "\n".join([
            "21 auditor/bot/a/1 UNKNOWN 2 1",
            "22 auditor/bot/a/2 UNKNOWN 2 1",
        ]) + "\n"
        result = subprocess.run(
            ["bash", "auditor/scripts/unstick-bot-prs.sh"],
            cwd=self.job,
            env={**self.env, "FAKE_GH_LIST": listing, "UNSTICK_UNKNOWN_WAIT_SECS": "0",
                 "FAKE_GH_MERGE_STATES": json.dumps({"21": "CLEAN"})},
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        merged = [c[2] for c in self.gh_calls() if c[:2] == ["pr", "merge"]]
        self.assertEqual(merged, ["21"])
        self.assertIn("#22", result.stdout)
        self.assertIn("still UNKNOWN", result.stdout)


if __name__ == "__main__":
    unittest.main()
