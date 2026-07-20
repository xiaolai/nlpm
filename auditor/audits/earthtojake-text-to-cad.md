# NLPM Audit: earthtojake/text-to-cad
**Date**: 2026-04-06  |  **Artifacts**: 24  |  **Strategy**: batched
**NL Score**: 95/100
**Security**: CLEAR
**Bugs**: 0  |  **Quality Issues**: 11  |  **Security Findings**: 3

## NL Score Summary

`skills/*` and `plugins/cad/skills/*` are byte-identical (verified via `diff` on
all 11 pairs — `plugins/cad/skills/` is a generated bundle copy produced by
`scripts/bundle/bundle-plugin.sh`, confirmed against `AGENTS.md`'s documented
symlink/bundle workflow). Both copies are scored per the task's file list;
scores are identical within each pair.

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/gcode/SKILL.md | Skill | 86/100 | Missing output format; vague quantifiers (`appropriate`, `relevant`) |
| plugins/cad/skills/gcode/SKILL.md | Skill (bundled) | 86/100 | Missing output format; vague quantifiers (`appropriate`, `relevant`) |
| skills/bambu-labs/SKILL.md | Skill | 88/100 | Missing output format |
| plugins/cad/skills/bambu-labs/SKILL.md | Skill (bundled) | 88/100 | Missing output format |
| skills/sendcutsend/SKILL.md | Skill | 92/100 | Vague quantifiers (4×: `relevant`, `as needed`) |
| plugins/cad/skills/sendcutsend/SKILL.md | Skill (bundled) | 92/100 | Vague quantifiers (4×: `relevant`, `as needed`) |
| skills/step-parts/SKILL.md | Skill | 94/100 | Vague quantifiers (3×: `relevant`) |
| plugins/cad/skills/step-parts/SKILL.md | Skill (bundled) | 94/100 | Vague quantifiers (3×: `relevant`) |
| skills/urdf/SKILL.md | Skill | 96/100 | Vague quantifiers (`relevant`, `appropriate`) |
| plugins/cad/skills/urdf/SKILL.md | Skill (bundled) | 96/100 | Vague quantifiers (`relevant`, `appropriate`) |
| skills/srdf/SKILL.md | Skill | 96/100 | Vague quantifiers (`relevant`, `when needed`) |
| plugins/cad/skills/srdf/SKILL.md | Skill (bundled) | 96/100 | Vague quantifiers (`relevant`, `when needed`) |
| skills/implicit-cad/SKILL.md | Skill | 96/100 | Vague quantifiers (2×: `relevant`) |
| plugins/cad/skills/implicit-cad/SKILL.md | Skill (bundled) | 96/100 | Vague quantifiers (2×: `relevant`) |
| skills/sdf/SKILL.md | Skill | 98/100 | Vague quantifier (`relevant`) |
| plugins/cad/skills/sdf/SKILL.md | Skill (bundled) | 98/100 | Vague quantifier (`relevant`) |
| skills/cad/SKILL.md | Skill | 98/100 | Vague quantifier (`relevant`) |
| plugins/cad/skills/cad/SKILL.md | Skill (bundled) | 98/100 | Vague quantifier (`relevant`) |
| skills/cad-viewer/SKILL.md | Skill | 100/100 | None |
| plugins/cad/skills/cad-viewer/SKILL.md | Skill (bundled) | 100/100 | None |
| skills/dxf/SKILL.md | Skill | 100/100 | None |
| plugins/cad/skills/dxf/SKILL.md | Skill (bundled) | 100/100 | None |
| CLAUDE.md | Memory import | 100/100 | None |
| plugins/cad/.claude-plugin/plugin.json | Plugin manifest | 100/100 | None |

Frontmatter (`name`, `description`) is present and complete on all 11 skills.
No agent/command-specific penalty categories apply (no `agents:`/`allowed-tools`
frontmatter on any of these SKILL.md files, and none declare `tools:`), so the
only applicable categories in this rubric were vague quantifiers (R01) and
missing output format (R16). `CLAUDE.md` is a thin `@AGENTS.md` importer,
matching NLPM's own recommended pattern for canonical cross-tool memory — no
penalty. `plugin.json` has all required/expected fields, and its version
(`0.3.9`) matches the canonical `plugins/cad/VERSION` and both marketplace
manifests.

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 1 |

The automated pre-scan reported 8 "critical pattern matches" against a
1147-file, repo-wide script inventory. A manual line-by-line read of every
script under `scripts/**` (41 `.sh` + 1 `.mjs`), all `.githooks/*`, the three
network/subprocess-capable skill executables directly invoked from SKILL.md
command blocks (`bambu_lan_print.py`, `gcode_tool.py`,
`download_step_part.py`), and every `package.json`/`requirements.txt` in the
repo found **no reproducible Critical or High pattern**: no curl-pipe-shell,
no `eval()`/`exec()` on untrusted input (the one `ast.literal_eval` hit is a
safe literal parser, not `eval`), no reverse shells, no base64-decode-and-run,
no `subprocess`/`Popen` with `shell=True` (both `subprocess.run` call sites
use list-form argv), no `os.system`, no `sudo`, and no credential
exfiltration to a non-owner endpoint. The pre-scan's 8 matches are most
plausibly false positives from its regex heuristics on things like the many
`.exec()` regex-method calls in bundled/vendored JS under `scripts/viewer/dist/`,
`ast.literal_eval`, or the TLS/token patterns below, which do match "risky
keyword" heuristics but are not exploitable as found. This is a downgrade
from the pre-scan's CRITICAL label to CLEAR after manual verification — treat
the pre-scan risk level as a triage prompt, not a confirmed verdict.

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks (NLPM `hooks/` convention) | 0 — none present |
| Git-native hooks (`.githooks/*`, `scripts/git-hooks/pre-commit`) | 6 (`pre-commit`, `post-commit`, `post-checkout`, `pre-push`, `post-merge`, `scripts/git-hooks/pre-commit`) — all standard git-lfs delegation or `bundle.sh --check`, no findings |
| Durable repo scripts (`scripts/**/*.{sh,mjs}`) | 42 (41 `.sh` + 1 `.mjs`), all reviewed |
| Skill-invoked network/subprocess executables | 3 (`skills/bambu-labs/scripts/bambu_lan_print.py`, `skills/gcode/scripts/gcode_tool.py`, `skills/step-parts/scripts/download_step_part.py`) |
| MCP configs (`.mcp.json`) | 0 — none present |
| `package.json` (excluding `node_modules`) | 14 across `packages/`, `viewer/`, `docs/`, and skill-bundled viewer copies — no `postinstall`/`preinstall` scripts found |
| `requirements.txt` | 16 across skills, `viewer/`, and repo root (`requirements-dev.txt`) — all unpinned (see LOW finding) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Medium | skills/bambu-labs/scripts/bambu_lan_print.py | 379 | SEC-tls-verify-disabled | `ssl.create_default_context()` followed by `check_hostname = False` and `verify_mode = ssl.CERT_NONE` for the printer's MQTT/FTPS TLS socket; same pattern repeats at lines 943-944, 1152-1153, 1210-1211. Mitigated: every call site is gated by `validate_local_host()` (line 329), which resolves the target and refuses non-private/non-loopback/non-link-local addresses unless `--allow-nonprivate-host` is explicitly passed (line 308's `is_local_address`). This is standard practice for Bambu Lab printers, which serve self-signed LAN certificates by firmware design — but the code accepts any cert, not just the printer's actual one, on the trusted subnet. |
| 2 | Medium | scripts/github-workflows/deploy-vercel-app.sh | 83 | SEC-env-token-network | `VERCEL_TOKEN` (from environment) is sent via `curl --header "Authorization: Bearer $VERCEL_TOKEN"` to `https://api.vercel.com`. This is expected, correctly-scoped CI/CD behavior (the token's own API, over HTTPS, in a workflow that requires `VERCEL_TOKEN`/`VERCEL_ORG_ID` to already be set) — flagged per the rubric's "environment variable access + network calls" pattern, not because it is exploitable. |
| 3 | Low | requirements-dev.txt | 22 | SEC-unpinned-semver | Every `requirements.txt` in the repo (`requirements-dev.txt`, `skills/{cad,cad-viewer,dxf,sdf,srdf,urdf}/requirements.txt`, `viewer/requirements.txt`, and their `plugins/cad/skills/*` mirrors) lists third-party packages (`ezdxf`, `playwright`, `networkx`, `lxml`, `pytest`, `trimesh`) with no version constraint at all — not even a semver range. `--editable` internal packages are excluded from this finding. |

No Critical or High findings.

## Bugs (PR-worthy)

No bugs found. Frontmatter is complete on every skill, every `references/*.md`
citation resolves to a real file (44 references checked across 11 skills, 0
missing), every `$skill-name` cross-reference resolves to an existing skill
directory, `plugin.json`'s `version` matches `plugins/cad/VERSION` and both
`marketplace.json` manifests, and `plugin.json`'s `skills: "./skills/"`
resolves to a `plugins/cad/skills/` directory containing all 11 skills
(including `bambu-labs`, which is easy to miss since it's absent from
`plugins/cad/skills/`'s otherwise-alphabetical near-match to `skills/` — it is
in fact present).

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | skills/bambu-labs/scripts/bambu_lan_print.py | TLS verification disabled for printer sockets (line 379 and 3 similar sites) | Not a drop-in fix — Bambu printers only offer self-signed certs, so blanket re-enabling verification would break every LAN connection. Lower-risk alternative: pin/verify the printer's certificate fingerprint on first use (TOFU) via the existing `serial`/cert-fetch path, or add a code comment at each `CERT_NONE` site cross-referencing `validate_local_host()` so the mitigation is documented in place rather than only in the caller. |
| 2 | requirements-dev.txt (and the 15 other requirements.txt files) | Unpinned dependency versions | Add minimum version bounds (e.g. `ezdxf>=1.3`) to catch breaking upstream releases before they reach `scripts/test/test.sh`; not urgent since these are dev/runtime tooling deps, not deployed-service deps. |

Finding #2 from the Security Findings table (Vercel token over HTTPS to
Vercel's own API) needs no fix — it is correct usage, not a defect.

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/gcode/SKILL.md | Missing output format — no "final response should include" statement (contrast with `sdf`'s "Required report shape" or `cad`'s/`dxf`'s "Final responses should include..." paragraphs) | -10 |
| 2 | skills/gcode/SKILL.md | Vague quantifiers: `appropriate` (line 41), `relevant` (line 63) | -4 |
| 3 | skills/bambu-labs/SKILL.md | Missing output format — no defined report/response shape despite being the highest-stakes skill in the repo (live printer control) | -10 |
| 4 | skills/bambu-labs/SKILL.md | Vague quantifier: `relevant` (line 33) | -2 |
| 5 | skills/sendcutsend/SKILL.md | Vague quantifiers: `relevant` (lines 22, 36), `as needed` (lines 39, 40) | -8 |
| 6 | skills/step-parts/SKILL.md | Vague quantifiers: `relevant` (lines 14, 23, 31) | -6 |
| 7 | skills/urdf/SKILL.md | Vague quantifiers: `relevant` (line 27), `appropriate` (line 38) | -4 |
| 8 | skills/srdf/SKILL.md | Vague quantifiers: `relevant` (line 26), `when needed` (line 33) | -4 |
| 9 | skills/implicit-cad/SKILL.md | Vague quantifiers: `relevant` (lines 136, 140) | -4 |
| 10 | skills/sdf/SKILL.md | Vague quantifier: `relevant` (line 37) | -2 |
| 11 | skills/cad/SKILL.md | Vague quantifier: `relevant` (line 76) | -2 |

`plugins/cad/skills/*` mirrors carry the identical issues at identical
line numbers (byte-identical files) and are not repeated as separate rows.

## Cross-Component

- `plugins/cad/skills/*` are exact byte-identical copies of `skills/*`
  (`diff` on all 11 pairs: zero differences), consistent with
  `scripts/bundle/bundle-plugin.sh`'s rsync-based generation and
  `AGENTS.md`'s documented develop-branch bundle workflow.
- Every `references/*.md` link cited from the 11 `SKILL.md` files resolves to
  an existing file (44 citations checked via `Glob`/`Grep` cross-check; 0
  missing).
- Every `$skill-name` cross-reference (`$cad`, `$cad-viewer`, `$dxf`,
  `$gcode`, `$bambu-labs`, `$sdf`, `$srdf`, `$step-parts`, `$sendcutsend`)
  resolves to an existing sibling skill directory. No orphaned or dangling
  skill references.
- `plugin.json`'s `version` (`0.3.9`) matches the canonical
  `plugins/cad/VERSION` file and both `.claude-plugin/marketplace.json` and
  the plugin's own manifest — no stale-version drift.
- `README.md`'s skill table lists all 11 skills with correct relative links,
  including `bambu-labs` and `implicit-cad` (both present, contrary to an
  initial skim of the file that suggested they might be missing from the
  table).
- No contradictions found between `AGENTS.md`'s stated repo rules (symlink
  layout, `packages/` as shared-code source of truth, `models/` as the sole
  artifact directory) and what the skill scripts and bundle tooling actually
  do.

## Recommendation

CLEAR — submit PRs for all bugs and medium/low security fixes. There are no
NL bugs to fix. Of the three security findings, only the unpinned-dependency
Low finding has a low-risk, uncontroversial fix; the TLS-verification Medium
finding needs a documentation-only PR (comment cross-referencing the existing
`validate_local_host()` mitigation) rather than a behavioral change, since a
behavioral fix would break legitimate LAN printer connections. The Vercel
token Medium finding needs no fix. The 11 Quality Issues (missing output
format on `bambu-labs`/`gcode`, vague quantifiers repo-wide) are informational
and below the bar for an unsolicited PR to an external maintainer, but are
worth surfacing if `earthtojake/text-to-cad` ever opts into NLPM scoring.
