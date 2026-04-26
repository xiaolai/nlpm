# NLPM Audit: nicobailon/visual-explainer
**Date**: 2026-04-06  |  **Artifacts**: 11  |  **Strategy**: single
**NL Score**: 66/100
**Security**: CLEAR
**Bugs**: 9  |  **Quality Issues**: 21  |  **Security Findings**: 4

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `commands/share.md` | command | 35 | No YAML frontmatter at all — both name and description missing |
| `commands/generate-slides.md` | command | 44 | Missing name (-25), no empty-input handling (-10), multi-step not numbered (-10) |
| `commands/generate-visual-plan.md` | command | 54 | Missing name (-25), no empty-input handling (-10) |
| `commands/generate-web-diagram.md` | command | 54 | Missing name (-25), no empty-input handling (-10) |
| `commands/plan-review.md` | command | 56 | Missing name (-25), no empty-input handling (-10) |
| `commands/diff-review.md` | command | 62 | Missing name (-25), vague quantifiers (-8) |
| `commands/project-recap.md` | command | 64 | Missing name (-25), vague quantifiers (-6) |
| `commands/fact-check.md` | command | 68 | Missing name (-25) |
| `SKILL.md` | skill | 88 | Scattered vague quantifiers — "key" used ~6 times without concrete threshold (-12) |
| `.claude-plugin/plugin.json` | plugin manifest | 100 | None |
| `plugins/visual-explainer/.claude-plugin/plugin.json` | plugin manifest | 100 | None |

**Weighted average**: (35+44+54+54+56+62+64+68+88+100+100) / 11 = **66/100**

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts | `install-pi.sh`, `plugins/visual-explainer/scripts/share.sh` |
| MCP configs | 0 |
| Package manifests | `package.json` (no scripts section — clean) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `install-pi.sh` | 13 | network-fetch-external-code | `git clone --depth 1 https://github.com/nicobailon/visual-explainer.git "$TEMP_DIR"` fetches and installs external code at runtime. URL is hardcoded (limits risk), but supply-chain compromise of the upstream repo would transparently deliver malicious content to installers. |
| 2 | Medium | `plugins/visual-explainer/scripts/share.sh` | 54 | network-deploy-public | `bash "$VERCEL_SCRIPT" "$TEMP_DIR"` deploys the user-supplied HTML file to a public Vercel URL. Any sensitive data embedded in the file becomes publicly accessible. VERCEL_SCRIPT is resolved from hardcoded paths, limiting injection risk. |
| 3 | Low | `install-pi.sh` | 23 | file-delete-fixed-path | `rm -rf "$SKILL_DIR"` removes `$HOME/.pi/agent/skills/visual-explainer` before reinstallation. Path is fully hardcoded; no user input involved. Risk is accidental wipe of skill data if the script is re-run unexpectedly. |
| 4 | Low | `install-pi.sh` | 28–30 | file-write-path-substitution | `sed -i "s\|{{skill_dir}}\|$SKILL_DIR\|g"` interpolates `$SKILL_DIR` (derived from `$HOME`) into a sed command using `\|` as delimiter. If `$HOME` contains `\|`, the sed expression breaks. Unlikely in practice but worth noting. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `commands/diff-review.md` | Missing `name` field in YAML frontmatter | Command registration may be incomplete in environments that require explicit name |
| 2 | `commands/fact-check.md` | Missing `name` field in YAML frontmatter | Same as above |
| 3 | `commands/generate-slides.md` | Missing `name` field in YAML frontmatter | Same as above |
| 4 | `commands/generate-visual-plan.md` | Missing `name` field in YAML frontmatter | Same as above |
| 5 | `commands/generate-web-diagram.md` | Missing `name` field in YAML frontmatter | Same as above |
| 6 | `commands/plan-review.md` | Missing `name` field in YAML frontmatter | Same as above |
| 7 | `commands/project-recap.md` | Missing `name` field in YAML frontmatter | Same as above |
| 8 | `commands/share.md` | No YAML frontmatter block at all — `name` missing | File is formatted as README documentation, not a command template; will not register as a command |
| 9 | `commands/share.md` | No YAML frontmatter block at all — `description` missing | Same root cause as #8 |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `install-pi.sh` | External git clone at install time — supply-chain risk if upstream repo is compromised | Pin to a specific commit SHA: `git clone --depth 1 <url> --branch <tag>` and document the expected SHA in a checksum file |
| 2 | `plugins/visual-explainer/scripts/share.sh` | Deployed HTML is public with no warning to the user in the pre-deploy output | Add an explicit `echo "⚠  Deployment is PUBLIC — anyone with the URL can view this file"` before deployment |
| 3 | `install-pi.sh` | sed delimiter clash possible if `$HOME` contains `\|` | Use a delimiter that cannot appear in a filesystem path, e.g., `#`: `sed -i "s#{{skill_dir}}#$SKILL_DIR#g"` |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | `commands/diff-review.md` | No `allowed-tools` declaration | -5 |
| 2 | `commands/fact-check.md` | No `allowed-tools` declaration | -5 |
| 3 | `commands/generate-slides.md` | No `allowed-tools` declaration | -5 |
| 4 | `commands/generate-visual-plan.md` | No `allowed-tools` declaration | -5 |
| 5 | `commands/generate-web-diagram.md` | No `allowed-tools` declaration | -5 |
| 6 | `commands/plan-review.md` | No `allowed-tools` declaration | -5 |
| 7 | `commands/project-recap.md` | No `allowed-tools` declaration | -5 |
| 8 | `commands/share.md` | No `allowed-tools` declaration | -5 |
| 9 | `commands/generate-slides.md` | No empty-input handling — `$@` with no fallback; invoking `/generate-slides` with no argument produces a broken prompt | -10 |
| 10 | `commands/generate-visual-plan.md` | No empty-input handling — `$@` with no fallback | -10 |
| 11 | `commands/generate-web-diagram.md` | No empty-input handling — `$@` with no fallback | -10 |
| 12 | `commands/plan-review.md` | No empty-input handling — `$1` (plan file) has no fallback if omitted | -10 |
| 13 | `commands/share.md` | No empty-input handling — `$1` shown as required with no graceful fallback in the command template | -10 |
| 14 | `commands/generate-slides.md` | Multi-step command (read → choose aesthetic → plan narrative → generate → write) described in bold paragraph headers but not explicitly numbered; a reader cannot see at a glance how many phases exist | -10 |
| 15 | `commands/diff-review.md` | Vague quantifiers: "comprehensive" (×1), "significant" (×2), "major" (×1) | -8 |
| 16 | `commands/generate-slides.md` | Vague quantifiers: "stunning" (×1), "distinctive" (×1), "compelling" (×1) | -6 |
| 17 | `commands/generate-visual-plan.md` | Vague quantifiers: "comprehensive" (×1), "relevant" (×1), "similar" (×1) | -6 |
| 18 | `commands/generate-web-diagram.md` | Vague quantifiers: "beautiful" (×1), "distinctive" (×1), "genuinely enhance" (×1) | -6 |
| 19 | `commands/project-recap.md` | Vague quantifiers: "comprehensive" (×1), "concise" (×1), "key" (×2) | -6 |
| 20 | `commands/plan-review.md` | Vague quantifiers: "comprehensive" (×1), "significant" (×1) | -4 |
| 21 | `SKILL.md` | "key" used ~6 times as a vague filter ("key snippets", "key metrics", "key invariants", "key function names", etc.) with no concrete threshold; each use leaves the agent to decide what qualifies | -12 |

## Cross-Component
- **Root vs. inner plugin.json version mismatch**: `.claude-plugin/plugin.json` (root, marketplace wrapper) declares version `1.0.0` while `plugins/visual-explainer/.claude-plugin/plugin.json` (the actual plugin) declares version `0.6.3`. If the marketplace wrapper is expected to mirror the plugin version, this is stale. If the two versions are intentionally independent, a comment in the root plugin.json would clarify intent.
- **`commands/share.md` format divergence**: Every other command uses a minimal YAML frontmatter block (`description:`) followed by a prompt template. `share.md` is written entirely as a README-style markdown document with headers, code fences, and sections. It does not function as a command template and does not follow the plugin's own command conventions.
- **All 8 commands missing `name`**: The missing `name` frontmatter field is a systemic gap across every command in the plugin, not a one-off oversight. A single PR adding `name: <filename-without-extension>` to each command's frontmatter would resolve all 8 bugs at once.
- **All internal references valid**: Every `./references/`, `./templates/`, and `./scripts/` path referenced in `SKILL.md` and the command files resolves to a real file in the repo. No broken relative paths.

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes.

**Suggested PR groupings:**
1. **Fix all command frontmatter** — add `name:` to 7 commands; rewrite `share.md` as a proper command template with YAML frontmatter. High signal-to-noise: single-line changes in each file, all from the same root cause.
2. **Empty-input handling** — add explicit fallback behavior for the 5 commands with unbounded `$@`/`$1` and no default. Minimal prose addition to each command.
3. **Security hardening in scripts** — pin the `git clone` to a tag/SHA, add the public-deployment warning, fix the sed delimiter. Low-risk changes, each < 3 lines.
