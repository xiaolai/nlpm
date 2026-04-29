# NLPM Audit: pe-menezes/fin-claude-plugin
**Date**: 2026-04-29  |  **Artifacts**: 8  |  **Strategy**: single
**NL Score**: 94/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 9  |  **Security Findings**: 3

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| agents/financeiro.md | agent | 80 | Zero examples (−15), no model declaration (−5) |
| skills/onboarding/SKILL.md | skill | 92 | Bash declared but unused (−3), two vague quantifiers (−4) |
| skills/fatura/SKILL.md | skill | 95 | Vague "tipicamente" without threshold (−2) |
| skills/conciliar/SKILL.md | skill | 96 | Vague "alguns reais" (softened by %-alternative) (−2) |
| skills/extrato/SKILL.md | skill | 96 | Unquantified "confiança baixa" (−2) |
| skills/instalar-fin-mcp/SKILL.md | skill | 97 | Very clean |
| skills/lancar/SKILL.md | skill | 97 | Vague "caso raro" (−2), otherwise clean |
| .claude-plugin/plugin.json | plugin manifest | 100 | None — NL penalties do not apply to JSON config |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 1 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 |
| Scripts (sh/py/js) | 0 |
| MCP configs | `.mcp.json` |
| Package manifests | 0 |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `.mcp.json` | 5 | SEC-unpinned-semver | `npx -y fin-app-mcp` has no version pin — any future npm release (including a compromised one) is silently adopted on next Claude restart |
| 2 | Medium | `.mcp.json` | 7 | SEC-network-call | MCP server contacts external API at `https://fin-app-wine.vercel.app`; expected behavior for a finance backend but documents a live external dependency |
| 3 | Low | `.mcp.json` | 4 | SEC-runtime-install | `npx -y` auto-downloads and executes npm package without user confirmation at each invocation; standard for MCP servers but worth noting |

## Bugs (PR-worthy)
No bugs found. All frontmatter fields required for registration (`name`, `description`) are present in every artifact. All cross-references from the agent to its skills resolve to existing files. No tools are called in skill bodies but absent from `allowed-tools`.

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `.mcp.json` | `fin-app-mcp` has no version pin (SEC-unpinned-semver) | Replace `"fin-app-mcp"` with `"fin-app-mcp@X.Y.Z"` where `X.Y.Z` is the current stable release (check `npm view fin-app-mcp version`); update intentionally on new releases |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | agents/financeiro.md | No example blocks — agent has zero input/output examples illustrating dispatch decisions | −15 |
| 2 | agents/financeiro.md | No `model` declaration in frontmatter — defaults silently to whatever Claude version is current | −5 |
| 3 | skills/onboarding/SKILL.md | `Bash` in `allowed-tools` but no explicit Bash command appears in skill body (closest usage is in `instalar-fin-mcp`) | −3 |
| 4 | skills/conciliar/SKILL.md | "alguns reais" (some reais) is a vague quantity for the rendimento-residual tolerance; the %-based alternative clause mitigates but does not eliminate the ambiguity | −2 |
| 5 | skills/extrato/SKILL.md | "se a confiança no parse for baixa" — no numeric or categorical threshold defined for what constitutes low confidence | −2 |
| 6 | skills/fatura/SKILL.md | "tipicamente até 3 meses antes" when searching for estorno originals — "tipicamente" is not actionable; should be a hard window | −2 |
| 7 | skills/lancar/SKILL.md | "caso raro" to describe when a saque should be treated as an expense — subjective, no decision criteria given | −2 |
| 8 | skills/onboarding/SKILL.md | "algo crítico" (Modo B validation step) — no definition of what makes a missing field critical vs. optional | −2 |
| 9 | skills/onboarding/SKILL.md | "muito próximas" for grouping establishment name variants — no edit-distance threshold or normalization algorithm specified | −2 |

## Cross-Component
All cross-component references are consistent:

- The agent (`agents/financeiro.md`) dispatches six slash commands — `/financeiro:onboarding`, `/financeiro:lancar`, `/financeiro:extrato`, `/financeiro:fatura`, `/financeiro:conciliar`, `/financeiro:instalar-fin-mcp` — and all six corresponding skill files exist in `skills/`.
- `plugin.json` declares `userConfig.fin_api_key` with `sensitive: true`; `.mcp.json` references it via `${user_config.fin_api_key}`, which is the correct Claude plugin interpolation pattern. No credential is hardcoded.
- All skills consistently reference the same four memory files (`Preferências.md`, `Contas e Cartões.md`, `Estabelecimentos.md`, `Status Conciliação.md`) with identical naming and path conventions.
- MCP tool names (`fin_criar_despesa`, `fin_buscar_transacoes`, `fin_criar_estorno`, etc.) are used consistently across the agent and all skills that call them.
- No orphan skills, no skill referenced by the agent but not present in the repo.

## Recommendation
CLEAR — submit PRs for all medium/low security fixes.

The plugin is well-engineered: clear dispatch logic, strong idempotency guarantees, thorough error-case coverage, and consistent memory conventions across six skills. The only meaningful quality gap is the agent having zero examples (−15), which makes it harder for new contributors to understand dispatch behavior without reading the full body. Adding two or three input/output examples to `agents/financeiro.md` and declaring a `model` tier would bring it to parity with the skills.

The single actionable security PR is pinning `fin-app-mcp` to a specific npm version in `.mcp.json`; this closes the supply-chain drift risk with a one-line change.
