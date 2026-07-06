# NLPM Audit: Graphify-Labs/graphify
**Date**: 2026-04-06  |  **Artifacts**: 8  |  **Strategy**: single
**NL Score**: 99/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 3  |  **Security Findings**: 2

## NL Score Summary

All 8 scored files live under `graphify/skills/agents/references/` — generated, on-demand reference
partials for the "agents" (generic AGENTS.md) platform overlay, built by `tools/skillgen` from a
shared fragment source and validated byte-for-byte in CI (`ci.yml` runs `python -m tools.skillgen
--check`). None of them are `SKILL.md`, `agents/*.md`, or `commands/*.md` under NLPM's own
classification rules (`commands/shared/classify.md`) — they classify as `document` (reference
partials loaded on demand), so the frontmatter/examples/model/allowed-tools penalties that apply to
SKILL.md bodies, subagents, and commands do not apply here. Scoring below applies the universal
floor (R01 vague quantifiers, R37 stale references) plus direct verification of every command,
function signature, CLI flag, and constant each file cites against the actual `graphify/*.py`
source.

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| github-and-merge.md | reference | 98/100 | Unbounded quantifier "several local subfolders" (R01) |
| query.md | reference | 98/100 | Unbounded quantifier "the appropriate traversal" (R01) |
| exports.md | reference | 95/100 | MCP tool list omits 3 of 10 tools the server actually registers |
| add-watch.md | reference | 100/100 | None |
| extraction-spec.md | reference | 100/100 | None |
| hooks.md | reference | 100/100 | None |
| transcribe.md | reference | 100/100 | None |
| update.md | reference | 100/100 | None |

Every runtime claim was cross-checked against source and confirmed accurate: `ingest()` /
`transcribe_all()` / `build_merge()` / `build_from_json()` / `detect_incremental()` /
`save_manifest()` / `graph_diff()` signatures, `graphify hook install/uninstall/status`, `graphify
agents install/uninstall`, `graphify save-result --question/--answer/--type/--nodes/--outcome/
--correction`, `graphify reflect --if-stale`, `GRAPHIFY_WHISPER_PROMPT`/`GRAPHIFY_WHISPER_MODEL` env
vars, the `graphifyy[video]` extras group, the six-value `file_type` enum
(`code|document|paper|image|rationale|concept` — matches `graphify/validate.py`
`VALID_FILE_TYPES` verbatim), and the node-ID stem-collapse rule (matches
`graphify/extractors/base.py::_file_stem` verbatim, including the `docs/v1/api/README.md` example).
No stale references, no broken links, no invented flags.

Two literal R01 hits were judgment-called as **false positives** and excluded from the score:
`extraction-spec.md` uses "reasonable inference" twice, but both are the fixed label for one point
on a fully-enumerated 5-value discrete confidence rubric (0.95/0.85/0.75/0.65/0.55, each with its
own concrete parenthetical definition) — not an unbounded quantifier. `query.md`'s "no relevant
vocabulary for this question" is verbatim output text the agent prints to the user, not an
instruction to the model. See the sidecar for both, marked `false_positive: true`.

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 1 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks (`hooks/**`) | 0 — none present |
| MCP configs (`.mcp.json`) | 0 — none present |
| Package manifests (`package.json`, `requirements.txt`) | 0 — pure `pyproject.toml` Python package, no Node tooling |
| Scripts (`.py`/`.sh`/`.js`, repo-wide — no dedicated `scripts/` dir exists) | ~185 files: `graphify/*.py` (library + CLI), `tools/skillgen/*.py` (build-time generator), `tests/*.py` (test suite), a handful of `.sh`/`.js` fixtures under `tests/fixtures/` and `worked/*/raw/` (sample corpora used as extraction test inputs, not executed by graphify itself) |

The requested glob patterns (`hooks/**`, `scripts/**/*.{sh,py,js}`, `.mcp.json`, `package.json`,
`requirements.txt`) all returned zero matches — this repo has no `hooks/` or `scripts/` directory
and ships no Node/pip manifest (dependencies live in `pyproject.toml`). The pre-scan's "204 scripts"
count reflects the whole `.py`/`.sh`/`.js` tree, not a dedicated build/install-script surface.
Targeted pattern search was run repo-wide instead (`os.system`, `subprocess(...shell=True)`,
`eval(`/`exec(`, `base64.b64decode`, `sudo`, `chmod 777`, `postinstall`, credential-to-network
exfiltration, `PATH` mutation) — no Critical or High hits. `graphify/security.py` independently
implements SSRF-guarded HTTP(S) connections (DNS-rebind-safe, resolves once and connects to the
validated IP), a private/reserved/CGN/NAT64-aware IP blocklist, scheme allowlisting (http/https
only), redirect re-validation, response-size caps, and HTML-safe metadata sanitization —
`SECURITY.md`'s claim of "does not use `shell=True` in any subprocess call" was verified true
(zero occurrences repo-wide).

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Medium | graphify/skills/agents/references/exports.md | 26 | Insecure-credential-example | Example shows `graphify export neo4j --push bolt://localhost:7687 --user neo4j --password PASSWORD` (and the FalkorDB equivalent) with the password inline on the CLI, never mentioning that the underlying CLI itself supports (and its own `--help` text recommends) `NEO4J_PASSWORD`/`FALKORDB_PASSWORD` env vars specifically to keep credentials off `argv`/shell history/`ps` output (see `graphify/__main__.py` lines ~4020-4027, comment references fix `F-031`). The doc teaches the exact pattern the CLI was hardened against. |
| 2 | Low | README.md | 116, 133 | curl-pipe-sh | `curl -LsSf https://astral.sh/uv/install.sh \| sh` — standard, human-run install instructions for the official `uv` installer (astral.sh, not attacker-controlled, not executed by any graphify automation). Flagged for completeness; judged not a real risk. See sidecar `false_positive: true`. |

## Bugs (PR-worthy)

No NL bugs found in the 8 scored files — no missing required fields, no broken cross-file
references, no invented CLI flags or function signatures.

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | graphify/skills/agents/references/exports.md | Neo4j/FalkorDB push examples put `--password PASSWORD` inline | Add a line noting `NEO4J_PASSWORD` / `FALKORDB_PASSWORD` env vars keep the password off argv/shell history, and prefer that form in the example when the user has already set the var |

Note: this same reference file is duplicated (via `tools/skillgen`) under
`graphify/skills/{amp,claude,claw,codex,copilot,droid,kilo,kiro,opencode,pi,trae,vscode,windows}/references/exports.md`
and its source fragment under `tools/skillgen/fragments/`. A real fix must land in the fragment
source so the generator re-propagates it to all 14 platform copies — hand-editing only the
`agents/` copy would be immediately reverted by CI's `--check` drift guard on the next
`skillgen` regeneration, and would leave 13 other platform copies with the same gap.

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | graphify/skills/agents/references/github-and-merge.md | R01 unbounded quantifier: "or named several local subfolders" (line 3) — no defined threshold for "several" | -2 |
| 2 | graphify/skills/agents/references/query.md | R01 unbounded quantifier: "Run the appropriate traversal from each starting node" (line 74) — decision criteria lives in the table above but isn't re-stated at the point of use | -2 |
| 3 | graphify/skills/agents/references/exports.md | MCP export section (Step 7d) lists 7 of the 10 tools `graphify/serve.py`'s `list_tools()` actually registers unconditionally — `list_prs`, `get_pr_impact`, and `triage_prs` are undocumented | -5 |

## Cross-Component

- **Multi-platform generation is consistent and CI-enforced.** All 8 files are generated by
  `tools/skillgen/gen.py` from shared fragments (`tools/skillgen/fragments/`) per
  `tools/skillgen/platforms.toml`, and `.github/workflows/ci.yml` runs `python -m tools.skillgen
  --check` (byte-diff against committed + `expected/` output) — so no independent per-platform drift
  is possible without failing CI. Spot-checked the platform-specific "commit hook + native memory
  file" wording: `skill-agents.md` (dispatcher for these 8 files) correctly says "native AGENTS.md
  integration", matching `hooks.md`'s actual content (`graphify agents install` writes to
  `AGENTS.md`) — no drift found there.
- **Minor step-summary omission (not a bug in the scored files themselves).** The root
  `graphify/skill.md` (Claude-platform dispatcher) describes `extraction-spec.md`'s content as
  covering "node-ID rules, confidence rubric, **frontmatter**, hyperedge, and vision rules", while
  the "agents"-platform dispatcher `skill-agents.md` drops "frontmatter" from that same summary
  line — even though the underlying `extraction-spec.md` reference file (scored here, identical
  across platforms) does document the YAML-frontmatter-copy rule. This is a one-word omission in a
  *different* file's (`skill-agents.md`) summary sentence, not a defect in any of the 8 scored
  reference files — noted for completeness, not scored.
- **MCP tool-list undercount** (see Quality Issues #3) is the one genuine content/code drift found:
  `exports.md` describes the MCP server's tool surface incompletely relative to `serve.py`.
- No orphaned files: all 8 references are reachable from `skill-agents.md`'s dispatch table, each
  gated behind the exact flag/condition the reference file itself declares at its top ("Load this
  when...").

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes. No bugs were found in the 8 scored
files, so the only outstanding item is the Medium security-fix suggestion (exports.md credential
example) plus the two minor R01 quality nits. Given the fragment/generator architecture, any
contribution must target `tools/skillgen/fragments/` (not the generated `graphify/skills/*/references/exports.md`
copies directly) and be validated with `python -m tools.skillgen --check` before submission.
