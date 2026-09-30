# NLPM Audit: LibreChat-AI/LibreChat
**Date**: 2026-04-06  |  **Artifacts**: 5  |  **Strategy**: single
**NL Score**: 99/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 2  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .claude/skills/improve-codebase-architecture/SKILL.md | skill | 96 | Vague quantifier ("a good stretch"); references skills `/grilling` and `/domain-modeling` not present in repo |
| .claude/skills/codebase-design/SKILL.md | skill | 98 | Vague quantifier ("a lot of behaviour") |
| e2e/fixtures/deployment-skills/e2e-deployment-skill/SKILL.md | skill (test fixture) | 100 | None |
| packages/api/src/agents/openai/README.md | documentation (not an NL artifact) | 100 | None |
| packages/api/src/agents/triggers/README.md | documentation (not an NL artifact) | 100 | None |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 3 |
| Medium | 1 |
| Low | 0 |

The pre-scan reported one Critical match. The only candidate I found is `search/healthcheck.sh:200`, a `/dev/tcp` probe of a local FerretDB port. It is a health check, not a reverse shell, so I recorded it as a false positive.

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | none (no `hooks/` dir) |
| MCP configs | none (`.mcp.json` absent) |
| Scripts | `scripts/redis-mode.sh`, `scripts/static-checks.mts`, `scripts/sort-imports.mts`, `scripts/merge-locize-download.mjs`, `scripts/validate-locize-download.mjs` |
| Ops scripts | `config/update.js`, `config/deployed-update.js`, `config/test-subdirectory-setup.sh`, `redis-config/start-cluster.sh`, `search/healthcheck.sh` |
| Package manifests | root `package.json` and workspace `package.json` files. No `postinstall` or `preinstall` script found. `requirements.txt` absent. |

Coverage note: the pre-scan counted 733 script files. I read only the files named above and ran repo-wide greps for the dangerous patterns. I did not read every script.

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | High | config/deployed-update.js | 39 | sudo usage | Runs `sudo docker compose ...` (lines 39, 46, 53, 60, 69, 73) in an operator-run deployment update script. The commands are intended, not malicious. |
| 2 | High | config/update.js | 70 | sudo usage | Optional `sudo ` prefix for docker commands, selected by a `useSudo` flag. |
| 3 | High | scripts/static-checks.mts | 321 | spawn with shell: true | `shell: true` is used only on win32 for the fixed `npm.cmd` executable. No user input reaches the shell. Low real risk. |
| 4 | Medium | config/deployed-update.js | 53 | command string interpolation | `sudo docker rmi ${imageRef}` is built from `docker images` output and run through a shell. Image names come from the local docker daemon, so injection is unlikely. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
No confirmed bugs.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | config/deployed-update.js | Shell-interpolated `docker rmi ${imageRef}` (line 53) | Use `execFileSync('sudo', ['docker', 'rmi', imageRef])` to avoid shell parsing. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | .claude/skills/improve-codebase-architecture/SKILL.md | Vague quantifier: "walk back a good stretch of the commit history" (line 23) | -2 |
| 2 | .claude/skills/codebase-design/SKILL.md | Vague quantifier: "a lot of behaviour behind a small interface" (line 8) | -2 |

## Cross-Component
- `.claude/skills/improve-codebase-architecture/SKILL.md` lines 64 and 66 invoke `/grilling` and `/domain-modeling`. Neither skill exists under `.claude/skills/`; only `codebase-design` and `improve-codebase-architecture` are present. They may be user-level skills. I could not verify this, so confidence is medium.
- The same skill references `CONTEXT.md` and `docs/adr/`. I did not check whether they exist, and the skill says to create `CONTEXT.md` lazily.
- Sibling links `DEEPENING.md`, `DESIGN-IT-TWICE.md` and `HTML-REPORT.md` all resolve to files on disk.
- `e2e-deployment-skill` uses `always-apply` and `user-invocable` frontmatter keys. I did not check them against the conventions; they are fixture-specific.

## Recommendation
BLOCKED — do not submit PRs. File private security report. The literal rule treats any High finding as blocking. In context, all three High findings are the repo's own operator and dev tooling (sudo docker, a Windows npm shim) and look benign. A human should confirm before any contribution is skipped permanently.
