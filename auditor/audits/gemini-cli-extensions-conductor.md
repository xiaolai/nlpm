# NLPM Audit: gemini-cli-extensions/conductor
**Date**: 2026-04-06  |  **Artifacts**: 6  |  **Strategy**: single
**NL Score**: 90/100
**Security**: REVIEW
**Bugs**: 1  |  **Quality Issues**: 26  |  **Security Findings**: 2

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/conductor-new-track/SKILL.md | Skill | 84/100 | Vague quantifiers — 8 occurrences (-16) |
| skills/conductor-revert/SKILL.md | Skill | 88/100 | Vague quantifiers — 6 occurrences (-12) |
| skills/conductor-status/SKILL.md | Skill | 88/100 | No worked example anywhere in the file (-10, R06) |
| skills/conductor-implement/SKILL.md | Skill | 89/100 | Vague quantifiers — 3 occurrences (-6) |
| skills/conductor-setup/SKILL.md | Skill | 92/100 | Vague quantifiers — 4 occurrences (-8) |
| skills/conductor-review/SKILL.md | Skill | 96/100 | Vague quantifiers — 2 occurrences (-4) |

All six files pass the hard frontmatter checks: `name`/`description` present, `name:` matches the parent directory, descriptions are specific and within length bounds, and body length is well under the 400-line R05 threshold (max 241 lines). No `-25`/`-15` structural penalties apply anywhere in this corpus.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none |
| Scripts | `skills/conductor-setup/scripts/resume.py` (1 file — read-only status check, no dangerous patterns) |
| MCP configs | none |
| Package manifests | none (`package.json`, `requirements.txt` absent) |
| Documented shell commands (agent-executed, not a script file) | `skills/conductor-setup/SKILL.md:182-187`, `skills/conductor-new-track/SKILL.md:126` — both instruct the agent to run `mkdir -p .agents/skills/<skill_name>` + `curl -sSL <URL>SKILL.md -o .agents/skills/<skill_name>/SKILL.md` |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Medium | skills/conductor-setup/SKILL.md | 182-187 | Network fetch / unpinned ref | Skill instructs the agent to `curl` a third-party `SKILL.md` from a URL sourced in `assets/catalog.md`, all of which point at `.../main/skills/<name>/` (a mutable branch head), then write it straight into `.agents/skills/<name>/SKILL.md`. The same section tells the user the skill "will be installed as a frozen version (commit \<sha\>)" (line 174/180), but no step anywhere resolves, embeds, or records a commit SHA — the safety claim is not implemented, so a later push to `main` on the third-party repo is fetched and trusted silently on the next install. |
| 2 | Medium | skills/conductor-new-track/SKILL.md | 126 | Network fetch / unpinned ref | Identical pattern to #1 — same unpinned `main`-branch catalog URLs, same unfulfilled "frozen version (commit \<sha\>)" promise (line 124), same missing SHA-resolution step. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/conductor-new-track/SKILL.md:126 | The "Execute Installation" step collapses `mkdir -p .agents/skills/<skill_name>` and `curl -sSL <URL>SKILL.md -o .agents/skills/<skill_name>/SKILL.md` into a single inline-code span prefixed with the literal word `bash`, instead of a fenced ` ```bash ` block on separate lines (the correctly-formatted version of the identical instruction exists at `skills/conductor-setup/SKILL.md:182-187`). | An agent or human told to run "exactly the following curl command sequence" gets an unusable, syntactically broken one-liner, breaking the skill-installation step of the New Track workflow. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | skills/conductor-setup/SKILL.md:182-187 | Curl install command fetches an unpinned `main`-branch URL while claiming commit-SHA pinning | Add a step that resolves the latest commit SHA for the skill's source repo (e.g. via the GitHub API or `git ls-remote`), rewrite the raw URL to include it (`.../<sha>/skills/<name>/SKILL.md`), and record the SHA alongside the installed skill so future runs can diff against it. |
| 2 | skills/conductor-new-track/SKILL.md:126 | Same unpinned-fetch gap as #1 | Same fix as #1; also fix the malformed code block (see Bugs #1) while touching this section. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/conductor-implement/SKILL.md:28 | Vague quantifier "properly" ("not initialized properly") without measurable criteria | -2 |
| 2 | skills/conductor-implement/SKILL.md:80 | Vague quantifier "relevant" ("If relevant skills are found") | -2 |
| 3 | skills/conductor-implement/SKILL.md:85 | Vague quantifier "appropriate" ("using appropriate question types") | -2 |
| 4 | skills/conductor-implement/SKILL.md (file-level) | No worked example anywhere for a multi-phase, branch-heavy protocol (handshake, track selection, doc-sync approval loop); only bare commit-message templates exist, no full illustrative scenario | -5 |
| 5 | skills/conductor-new-track/SKILL.md:30 | Vague quantifier "properly" | -2 |
| 6 | skills/conductor-new-track/SKILL.md:76 | Vague quantifier "relevant" ("Ask 3-4 relevant questions") | -2 |
| 7 | skills/conductor-new-track/SKILL.md:79 | Vague quantifier "relevant" ("Ask 3-4 relevant questions") | -2 |
| 8 | skills/conductor-new-track/SKILL.md:81 | Vague quantifier "relevant" ("Ask 2-3 relevant questions") | -2 |
| 9 | skills/conductor-new-track/SKILL.md:82 | Vague quantifier "sufficient" ("Is this sufficient information") | -2 |
| 10 | skills/conductor-new-track/SKILL.md:84 | Vague quantifier "sufficient" ("Once sufficient information is gathered") | -2 |
| 11 | skills/conductor-new-track/SKILL.md:117 | Vague quantifier "relevant" ("Identify any relevant skills") | -2 |
| 12 | skills/conductor-new-track/SKILL.md:121 | Vague quantifier "relevant" ("If relevant missing skills are found") | -2 |
| 13 | skills/conductor-revert/SKILL.md:28 | Vague quantifier "properly" | -2 |
| 14 | skills/conductor-revert/SKILL.md:56 | Vague quantifier "relevant" ("find relevant items") | -2 |
| 15 | skills/conductor-revert/SKILL.md:58 | Vague quantifier "relevant" ("most relevant Tracks, Phases, or Tasks") | -2 |
| 16 | skills/conductor-revert/SKILL.md:78 | Vague quantifier "relevant" ("modified the relevant Implementation Plan file") | -2 |
| 17 | skills/conductor-revert/SKILL.md:123 | Vague quantifier "relevant" ("read the relevant Implementation Plan file(s)") | -2 |
| 18 | skills/conductor-revert/SKILL.md:123 | Vague quantifier "correctly" ("has been correctly reset") | -2 |
| 19 | skills/conductor-review/SKILL.md:34 | Vague quantifier "properly" | -2 |
| 20 | skills/conductor-review/SKILL.md:74 | Vague quantifier "relevant" ("If relevant skills (e.g., gcp-*) are found") | -2 |
| 21 | skills/conductor-setup/SKILL.md:88 | Vague quantifier "relevant" ("Use git ls-files to identify relevant files") | -2 |
| 22 | skills/conductor-setup/SKILL.md:146 | Vague quantifier "appropriate" ("Select and copy appropriate style guides") | -2 |
| 23 | skills/conductor-setup/SKILL.md:171 | Vague quantifier "relevant" ("identify relevant skills NOT yet installed") | -2 |
| 24 | skills/conductor-setup/SKILL.md:177 | Vague quantifier "relevant" ("If relevant missing skills are found") | -2 |
| 25 | skills/conductor-status/SKILL.md:28 | Vague quantifier "properly" | -2 |
| 26 | skills/conductor-status/SKILL.md (file-level) | Zero worked examples of any kind (no sample rendered status report, no illustrative scenario) despite listing 7 required output fields | -10 |

## Cross-Component
- **README vs. shipped surface** (`README.md`, medium confidence): the README's "📋 Commands Reference" section and step-by-step guide document every skill as a slash command (`/conductor:conductor-setup`, `/conductor:conductor-new-track`, `/conductor:conductor-implement`, `/conductor:conductor-status`, `/conductor:conductor-revert`, `/conductor:conductor-review`), but the repository contains no `commands/` directory anywhere — only `skills/conductor-*/SKILL.md`. On hosts where Skills are auto-triggered by description match rather than explicitly slash-invocable (e.g. Claude Code without a `commands/` wrapper), the documented invocation syntax would not work as written. Exact behavior is host-dependent (Antigravity/Gemini CLI extension semantics may differ from Claude Code), so this is flagged at medium rather than high confidence.
- **Duplicated catalog file** (low confidence, informational): `skills/conductor-new-track/assets/catalog.md` and `skills/conductor-setup/assets/catalog.md` are byte-identical copies of the same Firebase/DevOps skill catalog. There is no single source of truth — updating one without the other will silently desynchronize the two skills' recommendation logic.
- Internal skill-to-skill handoffs (conductor-implement → conductor-setup/conductor-review, conductor-new-track → conductor-setup/conductor-implement, conductor-revert → conductor-setup, conductor-review → conductor-setup/conductor-revert/conductor-status, conductor-setup → conductor-new-track, conductor-status → conductor-setup) are all internally consistent — every skill referenced by name is one of the six shipped skills. No orphaned components.
- All `assets/` and `scripts/` paths referenced from the six SKILL.md files resolve to files that actually exist on disk (`assets/catalog.md`, `assets/code_styleguides/`, `assets/workflow.md`, `scripts/resume.py`).

## Recommendation
REVIEW — submit NL fix PRs (the malformed curl block in `conductor-new-track/SKILL.md`, plus the highest-value vague-quantifier cleanups), and flag the two unpinned-skill-fetch findings in a private issue/discussion with the maintainer rather than a public PR, since fixing them requires a maintainer decision on how to implement commit pinning.
