# Privacy Policy — NLPM

_Last updated: 2026-05-26_

NLPM analyzes natural-language artifacts inside your repository — locally. The slash-command surface (`/nlpm:*`) is delivered as a Claude Code plugin; the scoring rubric covers artifacts authored for Claude Code, Codex CLI, and Antigravity. The standalone Python validator (`bin/nlpm-check`) runs without Claude Code at all. This policy describes the data NLPM handles.

## What NLPM reads

The contents of files in your project (skills, agents, commands, rules, hooks, manifests) when you run any of: `/nlpm:ls`, `/nlpm:score`, `/nlpm:check`, `/nlpm:fix`, `/nlpm:test`, `/nlpm:security-scan`, `/nlpm:trend`. Also reads `.claude/nlpm.local.md` (per-project configuration) when present.

## What NLPM writes

`.claude/nlpm-history.json` — per-project snapshots of scores and component counts over time. Stored on your local filesystem; never transmitted. The standalone validator (`bin/nlpm-check`) reads and exits without writing.

## What NLPM transmits

**Nothing.** All scoring, checking, fixing, and testing runs locally through Claude Code. NLPM does not maintain its own backend, does not phone home, does not collect telemetry, does not register usage with any third party.

When Claude Code orchestrates the agents (scorer, scanner, checker, etc.), the artifact contents are sent to Anthropic's API **by Claude Code itself** — under Anthropic's privacy terms, using your own credentials. NLPM is not in that path.

## Third parties

Optional badge fetching from shields.io occurs only if you opt in by embedding the "Validated by NLPM" badge URL in your README. shields.io's privacy policy applies in that case.

## What about the auditor pipeline?

The `auditor/` directory inside the NLPM source repo runs a separate GitHub Actions pipeline that audits **other** public plugin and skill repositories (today: Claude Code plugins; Codex CLI and Antigravity discovery is planned). That pipeline runs on the maintainer's GitHub account, not on your machine. Installing NLPM as a plugin does **not** enroll your repository in that pipeline.

## Data deletion

There is no centralized data to delete on the maintainer's side. To remove local data: delete `.claude/nlpm-history.json` and `.claude/nlpm.local.md` from your projects, then `claude plugin uninstall nlpm@xiaolai`.

## Contact

For privacy questions or to report a discrepancy with this policy: **xiaolaiapple@gmail.com**.
