# NLPM Audit: tw93/Waza
**Date**: 2026-04-19  |  **Artifacts**: 13  |  **Strategy**: single
**NL Score**: 79/100
**Security**: BLOCKED
**Bugs**: 0  |  **Quality Issues**: 20  |  **Security Findings**: 2

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/check/agents/reviewer-architecture.md | Agent | 38 | No frontmatter (name, description); no model; one example |
| skills/check/agents/reviewer-security.md | Agent | 38 | No frontmatter (name, description); no model; one example |
| skills/health/agents/inspector-context.md | Agent | 38 | No frontmatter (name, description); no model; one example |
| skills/health/agents/inspector-control.md | Agent | 40 | No frontmatter (name, description); no model; one example |
| skills/health/SKILL.md | Skill | 96 | Vague: "relevant" used loosely ×2 |
| skills/check/SKILL.md | Skill | 97 | Vague: "obvious" once in scope check |
| CLAUDE.md | Project meta | 98 | Vague: "non-trivial" once |
| skills/design/SKILL.md | Skill | 98 | Vague: "genuinely" once |
| skills/hunt/SKILL.md | Skill | 98 | None significant |
| skills/learn/SKILL.md | Skill | 98 | None significant |
| skills/read/SKILL.md | Skill | 98 | None significant |
| skills/think/SKILL.md | Skill | 98 | Vague: "meaningful" once |
| skills/write/SKILL.md | Skill | 98 | None significant |

**Score calculation**: (38+38+38+40+96+97+98+98+98+98+98+98+98) / 13 = 1033 / 13 = **79/100**

The four agent instruction files dragging the average down are all structurally identical in their gap: they are written as raw system prompts with no YAML frontmatter. The nine skill and meta files are uniformly strong (96–98).

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 1 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Scripts | scripts/setup-statusline.sh, scripts/statusline.sh, scripts/verify-skills.sh |
| Hooks | none |
| MCP configs | none |
| Package manifests | none |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | scripts/setup-statusline.sh | 76–77 | Remote script download + chmod +x | `curl -fsSL "$RAW" -o "$DEST"` downloads `statusline.sh` from the unpinned `main` branch of the same repo to `~/.claude/statusline.sh`, then `chmod +x` makes it executable. Claude Code runs this file on every startup via the injected `statusLine` setting. If the `main` branch is ever compromised, malicious code executes silently in every user session. No integrity check (SHA hash or commit pin) guards the download. |
| 2 | MEDIUM | scripts/setup-statusline.sh | 76 | Network call without hash verification | `curl` fetches from `raw.githubusercontent.com` with `-fsSL` but no `--hash` or equivalent digest verification. Even without a branch compromise, a MITM attacker on an untrusted network (public Wi-Fi, corporate proxy) could substitute the payload. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No NL-artifact bugs found | — |

All required frontmatter fields are present in every registered SKILL.md. Reference files declared in skills (persona-catalog.md, design-reference.md, read-methods.md, write-zh.md, write-en.md) are validated by `scripts/verify-skills.sh` and not flagged broken. The four agent files (reviewer-*.md, inspector-*.md) are loaded as sub-agent context, not registered entries, so their missing frontmatter is a quality issue rather than a registration bug.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| — | — | Finding #1 (HIGH) requires private disclosure — do not submit a public PR | See recommendation |
| 1 | scripts/setup-statusline.sh | Finding #2 (MEDIUM): curl download without integrity check | Pin the download to a specific git tag or commit SHA. Replace `RAW="https://raw.githubusercontent.com/tw93/Waza/main/scripts/statusline.sh"` with a versioned URL (e.g., `https://raw.githubusercontent.com/tw93/Waza/v3.11.0/scripts/statusline.sh`) **and** add a SHA-256 check immediately after the download: `echo "<expected_sha256>  $DEST" \| sha256sum -c || { echo "Integrity check failed"; rm -f "$DEST"; exit 1; }` |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/check/agents/reviewer-architecture.md | Missing `name` frontmatter field | −25 |
| 2 | skills/check/agents/reviewer-architecture.md | Missing `description` frontmatter field | −25 |
| 3 | skills/check/agents/reviewer-architecture.md | No model tier declared | −5 |
| 4 | skills/check/agents/reviewer-architecture.md | Single output-format example; no second usage example | −5 |
| 5 | skills/check/agents/reviewer-security.md | Missing `name` frontmatter field | −25 |
| 6 | skills/check/agents/reviewer-security.md | Missing `description` frontmatter field | −25 |
| 7 | skills/check/agents/reviewer-security.md | No model tier declared | −5 |
| 8 | skills/check/agents/reviewer-security.md | Single output-format example; no second usage example | −5 |
| 9 | skills/health/agents/inspector-context.md | Missing `name` frontmatter field | −25 |
| 10 | skills/health/agents/inspector-context.md | Missing `description` frontmatter field | −25 |
| 11 | skills/health/agents/inspector-context.md | No model tier declared | −5 |
| 12 | skills/health/agents/inspector-context.md | Single output-format example; no second usage example | −5 |
| 13 | skills/health/agents/inspector-control.md | Missing `name` frontmatter field | −25 |
| 14 | skills/health/agents/inspector-control.md | Missing `description` frontmatter field | −25 |
| 15 | skills/health/agents/inspector-control.md | No model tier declared | −5 |
| 16 | skills/health/agents/inspector-control.md | Single output-format example; no second usage example | −5 |
| 17 | skills/health/SKILL.md | Vague quantifier "relevant" in "Give Agent 1 the relevant Step 1 sections" (line 81) and "Include only checks relevant to the detected tier" (line 98) — both could specify which sections by name | −2 × 2 = −4 |
| 18 | skills/check/agents/reviewer-architecture.md | Vague: "significantly worse by this diff" — no threshold defined | −2 |
| 19 | skills/check/agents/reviewer-security.md | Vague: "materially easier to exploit" — no threshold defined | −2 |
| 20 | skills/health/agents/inspector-context.md | Vague: "relevant Step 1 sections" (line 65) — could list them explicitly | −2 |

**Systemic note on issues 1–16**: All four agent files (`reviewer-architecture.md`, `reviewer-security.md`, `inspector-context.md`, `inspector-control.md`) are used as raw system prompts passed to sub-agents by their parent skills (`check/SKILL.md` and `health/SKILL.md`). Adding frontmatter and a model declaration to each would improve observability in tooling and make the agent quality machine-checkable (e.g., extending `verify-skills.sh` to cover `agents/` subdirectories).

## Cross-Component
**Automated quality gate covers skills but not agents.** `scripts/verify-skills.sh` enforces frontmatter, version parity, description conventions, and RESOLVER.md coverage for every `skills/*/SKILL.md`. The four agent files in `skills/check/agents/` and `skills/health/agents/` are not in scope for this script. Their quality issues (missing frontmatter, no model declaration) can silently regress without triggering verification failure. Extending the script's reference check to also lint `agents/*.md` files for frontmatter presence would close this gap.

**RESOLVER.md coverage enforced.** `verify-skills.sh` requires every skill to appear in `skills/RESOLVER.md`; CLAUDE.md documents this contract. The eight SKILL.md files audited all have matching entries (enforced mechanically).

**Reference file integrity checked.** `verify-skills.sh` verifies that all supporting reference files (design-reference.md, read-methods.md, write-zh.md, write-en.md, persona-catalog.md, and both inspector agents) exist before allowing a commit. No broken references observed in the 13 audited artifacts.

**health/SKILL.md sub-agent wiring consistent.** Lines 81 and 84 correctly reference `agents/inspector-context.md` and `agents/inspector-control.md`, both of which exist. The data flow description (Step 1 sections pasted inline, credentials redacted) matches what the agents expect in their input bundles.

**No contradictions between SKILL.md files.** The eight skills cover non-overlapping domains with explicit "Not for" exclusion clauses in every description. RESOLVER.md is the designated routing arbitrator; no description overlap that would cause misfired invocations was found.

## Recommendation
BLOCKED — do not submit PRs. File private security report.

`scripts/setup-statusline.sh` downloads an executable from an unpinned `main`-branch URL and installs it into a privileged location (`~/.claude/`) that Claude Code runs on every session startup. This is a HIGH-severity supply chain vector. Resolve it privately with the maintainer before any public contribution:

1. Report the HIGH finding to the maintainer via GitHub Security Advisories (private channel).
2. Suggest pinning the download to a versioned tag URL and adding a SHA-256 integrity check (see Security Fixes table for the exact patch).
3. Once the maintainer has acknowledged and either patched or accepted the risk, the NL quality issues (all informational, no bugs) can be raised as a follow-up PR or issue.

The NL artifact quality is strong (nine of thirteen files score ≥96). If the security concern is resolved, the only remaining contribution surface would be adding YAML frontmatter and model declarations to the four agent files — a low-risk, high-value improvement that would bring the repo's NL score to approximately 95/100.
