# NLPM Audit: PeonPing/peon-ping
**Date**: 2026-04-26  |  **Artifacts**: 98  |  **Strategy**: progressive
**NL Score**: 77/100
**Security**: REVIEW
**Bugs**: 3  |  **Quality Issues**: 18  |  **Security Findings**: 7

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| .gitban/agents/dispatcher/inbox/kr62ia-dispatch-log.md | inbox-message | 70 | Unresolved `$(date -u +...)` shell literal on line 9; vague timestamp placeholder |
| .gitban/agents/planner/inbox/HOOKLOG-77eri8-planner-1.md | inbox-message | 72 | Missing L2 item (only L1/L3/L4 listed — numbering gap, mildly ambiguous) |
| .gitban/agents/planner/inbox/HOOKLOG-r783op-planner-1.md | inbox-message | 74 | Low vague-word count; generally clear |
| .gitban/agents/planner/inbox/HOOKBUG-d5wz2f-planner-1.md | inbox-message | 74 | Low vague count; specific but "consider" appears 3× (-6) |
| .gitban/agents/planner/inbox/HOOKBUG-kydihy-planner-1.md | inbox-message | 74 | "consider" (x2) + "likely" (-6); otherwise well-scoped |
| .gitban/agents/planner/inbox/SMARTPACKDEBT-exg19y-planner-1.md | inbox-message | 74 | "consider" + "appropriate" (-4); precise otherwise |
| .gitban/agents/planner/inbox/SMARTPACKDEBT-dsmh31-planner-1.md | inbox-message | 76 | "consider" (x1) + "various" absent; clear |
| .gitban/agents/planner/inbox/WINFOCUS-w7eys1-planner-1.md | inbox-message | 76 | "consider" (x1); good specificity |
| .gitban/agents/planner/inbox/WINTRAIN-2twy3o-planner-1.md | inbox-message | 76 | "consider" (x1); specific cards |
| .gitban/agents/planner/inbox/HOOKLOG-unkjkl-planner-1.md | inbox-message | 78 | Minimal vague language; clear refactoring card |
| .gitban/agents/planner/inbox/HOOKLOG-u48cb6-planner-1.md | inbox-message | 78 | Clear timestamp + newline issues; concise |
| .gitban/agents/planner/inbox/SMARTPACKDEBT-inexon-planner-2.md | inbox-message | 78 | "defensive", "appropriate" (x2) (-4) |
| .gitban/agents/planner/inbox/SMARTPACKDEBT-inexon-planner-1.md | inbox-message | 78 | "appropriate" (x1) (-2); otherwise precise |
| .gitban/agents/planner/inbox/WINTRAIN-hchc5z-planner-1.md | inbox-message | 78 | "proper" absent; "relevant" (x1) (-2) |
| .gitban/agents/planner/inbox/WINFOCUS-afe3sm-planner-1.md | inbox-message | 78 | "sufficient" absent; "consider" (x2) (-4) |
| .gitban/agents/planner/inbox/kr62ia-kr62ia-planner-1.md | inbox-message | 78 | "align" (x1); otherwise clear |
| .gitban/agents/planner/inbox/HOOKLOG-kt3ucx-planner-1.md | inbox-message | 78 | Clear two-card format; no significant vague words |
| .gitban/agents/planner/inbox/SMARTPACK-9pjhy5-planner-1.md | inbox-message | 78 | "consider" (x2) (-4); specific technical detail |
| .gitban/agents/planner/inbox/HOOKLOG-kt3ucx-planner-1.md | inbox-message | 78 | Clear two-card format |
| .gitban/agents/planner/inbox/SMARTPACK-aodz7v-planner-1.md | inbox-message | 80 | Clean single-card; no vague language |
| .gitban/agents/planner/inbox/SMARTPACK-janrlf-planner-1.md | inbox-message | 80 | Clean two-card; minor "consider" (x1) (-2) |
| .gitban/agents/planner/inbox/SMARTPACK-i0u93q-planner-1.md | inbox-message | 80 | Clean two-card; "consider" (x1) (-2) |
| .gitban/agents/planner/inbox/WINTRAIN-yq8iba-planner-1.md | inbox-message | 80 | Clean two-card; no significant vague words |
| .gitban/agents/planner/inbox/SMARTPACK-z0c9fd-planner-1.md | inbox-message | 82 | Single focused card; clear instructions |
| .gitban/agents/planner/inbox/WINTEST-f4w9gu-planner-1.md | inbox-message | 82 | Single card; precise edge case description |
| .gitban/agents/planner/inbox/HOOKLOG-unkjkl-planner-1.md | inbox-message | 82 | Clear DRY refactoring task |
| .gitban/agents/planner/inbox/WINTRAIN-yq8iba-planner-1.md | inbox-message | 82 | Clear Pester test scope |
| .gitban/agents/planner/inbox/HOOKLOG-r783op-planner-1.md | inbox-message | 82 | Two cards; clear scoping |
| .gitban/agents/planner/inbox/HOOKLOG-77eri8-planner-1.md | inbox-message | 82 | Three items; test fixture focus |
| .gitban/agents/planner/inbox/WINFOCUS-w7eys1-planner-1.md | inbox-message | 82 | Clear behavioral mock description |
| .gitban/agents/executor/inbox/HOOKLOG-u48cb6-executor-1.md | inbox-message | 80 | Refactoring instructions with 3 explicit blockers; clear |
| .gitban/agents/executor/inbox/SMARTPACKDEBT-inexon-executor-1.md | inbox-message | 76 | 6 blockers; thorough but "properly" absent; "appropriate" (x1) (-2) |
| .gitban/agents/executor/inbox/WINTEST-od5a0c-executor-1.md | inbox-message | 80 | Clear rejection; "fabricated" framing direct; no vague language |
| .gitban/agents/executor/inbox/HOOKLOG-px9k89-executor-1.md | inbox-message | 78 | 3 blockers; clear refactoring; "trivially" (-2) |
| .gitban/agents/executor/inbox/HOOKLOG-77eri8-executor-1.md | inbox-message | 84 | Close-out with specific fix; clear |
| .gitban/agents/executor/inbox/HOOKLOG-nnj6gt-executor-1.md | inbox-message | 86 | Clean close-out; no issues |
| .gitban/agents/executor/inbox/SMARTPACKDEBT-inexon-executor-2.md | inbox-message | 86 | Clean approved close-out |
| .gitban/agents/executor/inbox/HOOKLOG-w56sog-executor-1.md | inbox-message | 84 | Two L-items with specific fixes; clear |
| .gitban/agents/executor/inbox/WINTRAIN-yq8iba-executor-1.md | inbox-message | 84 | Specific L1 fix with line numbers |
| .gitban/agents/executor/inbox/WINFOCUS-afe3sm-executor-1.md | inbox-message | 84 | Specific close-out items |
| .gitban/agents/executor/inbox/HOOKBUG-d5wz2f-executor-1.md | inbox-message | 84 | Specific cosmetic fix |
| .gitban/agents/executor/inbox/SMARTPACKDEBT-exg19y-executor-1.md | inbox-message | 86 | Clean close-out |
| .gitban/agents/executor/inbox/HOOKBUG-kydihy-executor-1.md | inbox-message | 86 | Clean close-out |
| .gitban/agents/executor/inbox/HOOKLOG-8v56dp-executor-1.md | inbox-message | 86 | Clean close-out; no issues |
| .gitban/agents/executor/inbox/kr62ia-io43px-executor-1.md | inbox-message | 86 | Clean close-out |
| .gitban/agents/executor/inbox/SMARTPACKDEBT-dsmh31-executor-1.md | inbox-message | 84 | Specific cosmetic fix |
| .gitban/agents/executor/inbox/WINFOCUS-w7eys1-executor-1.md | inbox-message | 86 | Clean close-out |
| .gitban/agents/executor/inbox/WINTEST-od5a0c-executor-2.md | inbox-message | 86 | Clean close-out |
| .gitban/agents/executor/inbox/SMARTPACK-0vvvnb-executor-1.md | inbox-message | 86 | Clean close-out |
| .gitban/agents/executor/inbox/SMARTPACK-3b0gx7-executor-1.md | inbox-message | 86 | Clean close-out |
| .gitban/agents/executor/inbox/HOOKLOG-unkjkl-executor-1.md | inbox-message | 84 | L2 fix with specific implementation guidance |
| .gitban/agents/executor/inbox/HOOKLOG-j6lzi1-executor-1.md | inbox-message | 86 | Clean close-out |
| .gitban/agents/executor/inbox/HOOKLOG-261745-executor-1.md | inbox-message | 86 | Clean close-out |
| .gitban/agents/executor/inbox/WINTEST-f4w9gu-executor-3.md | inbox-message | 84 | Specific close-out with stale note fix |
| .gitban/agents/executor/inbox/HOOKLOG-px9k89-executor-1.md | inbox-message | 78 | Rejection with 3 blockers; clear |
| .gitban/agents/executor/inbox/SMARTPACKDEBT-inexon-executor-1.md | inbox-message | 76 | 6 blockers; thorough |
| .gitban/agents/executor/inbox/HOOKLOG-8v56dp-executor-1.md | inbox-message | 86 | Clean doc close-out |
| .gitban/agents/executor/inbox/WINTRAIN-hchc5z-executor-1.md | inbox-message | 86 | (via WINTRAIN dispatch reference) |
| .gitban/agents/executor/inbox/WINTRAIN-2twy3o-executor-1.md | inbox-message | 86 | (via WINTRAIN dispatch reference) |
| .gitban/agents/executor/inbox/HOOKLOG-px9k89-executor-2.md | inbox-message | 80 | Rework instructions; clear |
| .gitban/agents/executor/inbox/SMARTPACK-aodz7v-executor-1.md | inbox-message | 86 | Clean |
| .gitban/agents/executor/inbox/HOOKLOG-261745-executor-1.md | inbox-message | 86 | Clean |
| .gitban/agents/executor/inbox/SMARTPACKDEBT-dsmh31-executor-1.md | inbox-message | 84 | Specific cosmetic fix |
| .gitban/agents/executor/inbox/WINTRAIN-yq8iba-executor-1.md | inbox-message | 84 | L1 with specific line numbers |
| .gitban/agents/executor/inbox/HOOKLOG-w56sog-executor-1.md | inbox-message | 84 | Two L-items |
| .gitban/agents/executor/inbox/HOOKLOG-77eri8-executor-1.md | inbox-message | 84 | L2 fix with clear instruction |
| .gitban/agents/executor/inbox/WINTEST-f4w9gu-executor-3.md | inbox-message | 84 | Specific close-out note |
| .gitban/agents/reviewer/inbox/TECHDEBT-laimst-reviewer-1.md | inbox-message | 82 | Review with backlog; "acceptable tradeoff" slightly vague but contextual |
| .gitban/agents/reviewer/inbox/HOOKLOG-r0qoai-reviewer-1.md | inbox-message | 85 | Thorough approval review; no significant issues |
| .gitban/agents/reviewer/inbox/HOOKLOG-ki3aim-reviewer-1.md | inbox-message | 85 | Thorough approval with detailed analysis |
| .gitban/agents/reviewer/inbox/HOOKLOG-oln59n-reviewer-1.md | inbox-message | 85 | Clean review; well-structured |
| .gitban/agents/reviewer/inbox/HOOKLOG-u48cb6-reviewer-2.md | inbox-message | 84 | Detailed blocker resolution review; "proportionality applies" slight vague |
| .gitban/agents/reviewer/inbox/TECHDEBT-csedqi-reviewer-2.md | inbox-message | 84 | Clear approval; specific code references |
| .gitban/agents/reviewer/inbox/HOOKLOG-80usvr-reviewer-1.md | inbox-message | 84 | Thorough; "minor asymmetry" contextual |
| .gitban/agents/reviewer/inbox/HOOKLOG-px9k89-reviewer-1.md | inbox-message | 82 | Rejection review; clear blockers; "richer" (-2) |
| .gitban/agents/reviewer/inbox/HOOKLOG-px9k89-reviewer-3.md | inbox-message | 84 | Approval; specific commit analysis |
| .gitban/agents/reviewer/inbox/TECHDEBT-d3c6b0-reviewer-1.md | inbox-message | 84 | Clear approval; precise |
| .gitban/agents/reviewer/inbox/TECHDEBT-n5uqeo-reviewer-1.md | inbox-message | 84 | Clear test precision review |
| .gitban/agents/reviewer/inbox/HOOKLOG-8v56dp-reviewer-1.md | inbox-message | 85 | Clean doc review; thorough |
| .gitban/agents/reviewer/inbox/HOOKLOG-ah4y1j-reviewer-1.md | inbox-message | 85 | Version bump review; "well-categorized" slightly subjective |
| .gitban/agents/reviewer/inbox/HOOKLOG-kt3ucx-reviewer-1.md | inbox-message | 82 | Rejection with 3 blockers + 2 follow-ups; specific |
| .gitban/agents/planner/inbox/HOOKLOG-r783op-planner-1.md | inbox-message | 82 | Two card output; clear |
| .gitban/agents/planner/inbox/HOOKLOG-288ewn-planner-1.md | inbox-message | 80 | Single card with 2 specific items |
| .gitban/agents/planner/inbox/HOOKLOG-u48cb6-planner-2.md | inbox-message | 82 | Duplicate deduplication note; clear |
| .gitban/agents/planner/inbox/HOOKLOG-2d99d1-planner-1.md | inbox-message | 82 | Single card |
| .gitban/agents/dispatcher/inbox/HOOKLOG-dispatch-log.md | inbox-message | 82 | Comprehensive sprint log; good structure; minor vague entries in timing |
| .gitban/agents/dispatcher/inbox/M2CLOSE-dispatch-log.md | inbox-message | 82 | Sprint log with metrics |
| .gitban/agents/dispatcher/inbox/HOOKBUG-dispatch-log.md | inbox-message | 82 | Sprint log; clear phase tracking |
| .gitban/agents/dispatcher/inbox/SMARTPACKDEBT-dispatch-log.md | inbox-message | 82 | Sprint log; clear |
| .gitban/agents/dispatcher/inbox/SMARTPACK-dispatch-log.md | inbox-message | 80 | Sprint log; "Recovered from interrupted session" slightly vague for Phase 3 |
| .gitban/agents/dispatcher/inbox/WINFOCUS-dispatch-log.md | inbox-message | 82 | Clear phase tracking |
| .gitban/agents/dispatcher/inbox/WINTRAIN-dispatch-log.md | inbox-message | 82 | Clear sequential sprint log |
| .gitban/agents/dispatcher/inbox/WINTEST-dispatch-log.md | inbox-message | 78 | More rework cycles; "fabricated evidence" appropriately direct; complex history |
| CLAUDE.md | instructions | 82 | Solid developer guide; "proactively suggest" slightly vague; cross-repo references to external repos |
| skills/peon-ping-config/SKILL.md | skill | 88 | Well-structured; missing explicit output format section; examples present |
| skills/peon-ping-rename/SKILL.md | skill | 86 | Good structure; no explicit model declaration; examples present |
| skills/peon-ping-toggle/SKILL.md | skill | 88 | Well-structured; examples present; no explicit output format |
| skills/peon-ping-use/SKILL.md | skill | 90 | Best of class; full manual fallback; examples; clear error handling |
| skills/peon-ping-log/SKILL.md | skill | 84 | Short skill; missing output format section; examples minimal; `ensure` absent |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 6 |
| Low | 1 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hook scripts (bash) | scripts/hook-handle-use.sh, scripts/hook-handle-rename.sh, scripts/remote-hook.sh |
| Hook scripts (PowerShell) | scripts/hook-handle-use.ps1 |
| Runtime hook | peon.sh (embedded Python), peon.ps1 (embedded PS hook) |
| Installer | install.sh, install.ps1 |
| Pack downloader | scripts/pack-download.sh |
| Notification/UI | scripts/notify.sh, scripts/win-notify.ps1 |
| Audio | scripts/win-play.ps1 |
| TTS | scripts/tts-native.sh, scripts/tts-native.ps1 |
| Overlay (JXA/JS) | scripts/mac-overlay.js, scripts/mac-overlay-glass.js, scripts/mac-overlay-jarvis.js, scripts/mac-overlay-sakura.js |
| Swift binaries | scripts/meeting-detect.swift, scripts/peon-play.swift |
| Lint tool | scripts/lint-python-quoting.sh |
| Utilities | scripts/install-utils.ps1 |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | scripts/pack-download.sh | 152 | curl + registry fetch | Fetches remote JSON from `peonping.github.io/registry/index.json` over HTTPS without pinning or integrity check. Registry controls `source_repo`, `source_ref`, and `source_path` fields used to construct download URLs. A compromised or MITMed registry could redirect downloads to attacker-controlled repos. Input validation (`is_safe_source_repo`, `is_safe_source_ref`) limits exploit surface but does not prevent a legitimate-looking repo substitution. |
| 2 | Medium | scripts/pack-download.sh | 406 | curl to GitHub raw | Downloads `openpeon.json` manifests and sound files from `raw.githubusercontent.com`. Files are written to `~/.claude/hooks/peon-ping/packs/`. SHA256 checksums are stored locally but only checked on cache hits, not on first download. Manifest content (file names, paths) is then parsed and used to construct further download URLs. A tampered manifest could cause unexpected file writes within the packs subdirectory. The `is_safe_filename` validator mitigates path traversal but uses a permissive charset that allows slashes in subdirectory creation. |
| 3 | Medium | scripts/notify.sh | 452 | Inline PowerShell exec via bash | The WSL legacy popup path constructs a multi-line PowerShell command string that interpolates bash variables (`$rgb_r`, `$rgb_g`, `$rgb_b`, `$dismiss_secs`, `$icon_win_path`, `$y_offset`) directly into the `-Command` string. The message itself is passed via a temp file (correct). However, `$icon_win_path` derives from `wslpath -w "$icon_path"` which could contain characters that break the PowerShell string literal. The `is_safe_filename` check in pack-download.sh does not apply here. |
| 4 | Medium | scripts/notify.sh | 566 | Inline PowerShell exec via bash (MSYS2) | Same pattern as finding #3 but for MSYS2/MinGW path. `$toast_xml_win` (from `cygpath -w`) is interpolated into PowerShell command string. Low exploit potential in practice but structurally unsound. |
| 5 | Medium | scripts/remote-hook.sh | 40 | curl to relay | Sends `CATEGORY` value to `localhost:19998/play?category=${CATEGORY}`. The category is derived from a hardcoded case statement, so the value is not user-controlled. Low practical risk but the relay endpoint is unauthenticated and the CATEGORY is part of the URL query string. If the category mapping ever becomes dynamic, this becomes a SSRF/injection vector. Currently safe. |
| 6 | Medium | scripts/pack-download.sh | 89 | python3 -c with interpolated path | At line 89, `python3 -c "import hashlib; print(hashlib.sha256(open('$(py_path "$1")','rb').read()).hexdigest())"` interpolates a filename into a double-quoted Python string. The `py_path` function returns a MSYS2 Windows path. If a filename contained a single quote, it would break the Python string literal. The `is_safe_filename` validator would normally prevent this, but it allows `!`, `?`, spaces, and parentheses which could be problematic on some shells. |
| 7 | Low | scripts/pack-download.sh | 24 | Hardcoded fallback ref | `FALLBACK_REF="v1.1.0"` is a pinned release tag — good practice. However, `FALLBACK_REPO="PeonPing/og-packs"` is hardcoded. If the `PeonPing` GitHub org were compromised, the fallback path would silently download from the compromised repo with no alternative. Consider documenting the fallback source and providing a mechanism to override it. |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | .gitban/agents/dispatcher/inbox/kr62ia-dispatch-log.md | Line 9 contains a literal unexpanded shell expression `$(date -u +"%Y-%m-%dT%H:%M:%SZ")` in the markdown body — appears to be a copy-paste of a template where the date was never substituted. | Cosmetic; the dispatch log shows a shell literal instead of an actual timestamp for the kr62ia executor dispatch date. Makes the log misleading. |
| 2 | skills/peon-ping-config/SKILL.md | `user_invocable: false` but the file is listed in CLAUDE.md under "Skills" as user-accessible via `/peon-ping-config`. This inconsistency means Claude Code may not surface the skill in autocomplete. | Users may not be able to invoke `/peon-ping-config` if the runtime respects `user_invocable: false`. |
| 3 | skills/peon-ping-log/SKILL.md | Uses hardcoded `~/.claude/hooks/peon-ping/peon.sh` path rather than the `${CLAUDE_CONFIG_DIR:-$HOME/.claude}` pattern used consistently in all other skills (peon-ping-toggle, peon-ping-use, peon-ping-config). | Log skill breaks for users with non-default `CLAUDE_CONFIG_DIR`, including Cursor users. |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | scripts/pack-download.sh | No integrity verification on first download of sound files; checksums are only used for cache validation on subsequent runs. | After downloading each sound file, compute its SHA256 and store it in `.checksums` (already done via `store_checksum`). Add an optional `expected_checksums` field in `openpeon.json` manifests; if present, verify against it. Alternatively, use `curl --max-filesize` to limit blast radius. |
| 2 | scripts/notify.sh | Variables `$rgb_r`, `$rgb_g`, `$rgb_b`, `$icon_win_path`, `$y_offset`, `$dismiss_secs` interpolated directly into PowerShell `-Command` string. | Pass all bash-derived values via temp file or PowerShell `-File` with named parameters, the same approach used for `$msg` (already safe). |
| 3 | scripts/pack-download.sh | `py_path` interpolation in `python3 -c` (line 89). | Use `sys.argv[1]` to pass the path: `python3 -c 'import hashlib, sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$(py_path "$1")"` |

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/peon-ping-config/SKILL.md | Missing explicit output format section — document specifies behavior but no "Output" heading. | -10 |
| 2 | skills/peon-ping-toggle/SKILL.md | Missing explicit output format section. | -10 |
| 3 | skills/peon-ping-rename/SKILL.md | No `model` field in frontmatter. | -5 |
| 4 | skills/peon-ping-config/SKILL.md | No `model` field in frontmatter. | -5 |
| 5 | skills/peon-ping-toggle/SKILL.md | No `model` field in frontmatter. | -5 |
| 6 | skills/peon-ping-log/SKILL.md | No `model` field in frontmatter; missing output format section. | -15 |
| 7 | skills/peon-ping-log/SKILL.md | Uses hardcoded `~/.claude/` path; other skills use `${CLAUDE_CONFIG_DIR:-$HOME/.claude}`. | -3 (path consistency) |
| 8 | CLAUDE.md | "proactively suggest a version bump" — "proactively" is mildly vague but acceptable in context. | -2 |
| 9 | .gitban/agents/dispatcher/inbox/SMARTPACK-dispatch-log.md | Phase 3 note "Recovered from interrupted session" with "code intact" claim but no verification method described. | -4 |
| 10 | .gitban/agents/dispatcher/inbox/WINTEST-dispatch-log.md | Multiple rework cycles documented; "executor claimed all items stale (fabricated evidence)" — terminology appropriate but jarring without context. | -2 |
| 11 | .gitban/agents/dispatcher/inbox/kr62ia-dispatch-log.md | Unresolved shell expression `$(date ...)` literal on line 9. | -4 |
| 12 | Various planner inbox files | "consider" used as instruction verb (should use imperative: "implement", "add", "refactor") — appears 15+ times across planner messages, each -2, capped at -20. | -20 (cap) |
| 13 | Various reviewer inbox files | "appropriate" used 8+ times in reviewer messages. | -8 (4 instances across files, -2 each) |
| 14 | Various inbox files | "ensure" used as verb (vague imperative). | -6 (3 instances) |
| 15 | Various inbox files | "relevant" used (e.g. "relevant section"). | -2 |
| 16 | skills/peon-ping-rename/SKILL.md | Missing explicit output format section. | -10 |
| 17 | CLAUDE.md | Cross-repo references to `../openpeon/`, `../homebrew-tap/`, `peonping-x-bot` that are outside this repo. Rules reference external files that auditors cannot verify. | info |
| 18 | skills/peon-ping-use/SKILL.md | Mentions "Cursor compatibility note" as a feature divergence without linking to a canonical design doc. Minor. | -0 (info) |

## Cross-Component

**Skill-to-hook consistency**: `skills/peon-ping-config/SKILL.md` sets `user_invocable: false` but `CLAUDE.md` documents it as a user-accessible skill invoked via `/peon-ping-config`. This is a direct contradiction that should be resolved (likely the skill should be `user_invocable: true`, or the CLAUDE.md should clarify the delegation model).

**Path inconsistency in skills**: `skills/peon-ping-log/SKILL.md` uses `~/.claude/hooks/peon-ping/peon.sh` (hardcoded) while all other skills use `${CLAUDE_CONFIG_DIR:-$HOME/.claude}`. The peon-ping-rename SKILL.md also references `~/.claude/hooks/peon-ping/.state.json` in the manual fallback example code — this should use the config dir pattern.

**CLAUDE.md cross-repo enforcement rules**: The "Change Enforcement Rules" section references files in peer repositories (`../openpeon/`, `../homebrew-tap/`) that are not part of this repository. An AI agent working from a fresh clone would have no access to verify these. The rules are correct and useful for human developers but create a verification gap for automated code review.

**Inbox message format consistency**: Close-out executor messages consistently use `Use .venv/Scripts/python.exe` or `Activate your venv first` headers on Windows branches but not Unix branches — this is a platform-appropriate inconsistency, not a bug, but worth noting for cross-platform parity of tooling instructions.

**`debug_retention_days` config key**: As documented across multiple planner messages (HOOKLOG-kt3ucx-planner-1.md, HOOKLOG-kt3ucx-reviewer-1.md L1), the `debug_retention_days` key was added to `config.json` and backfilled in `peon update` but the log rotation implementation was tracked as a separate card (px9k89). Per the HOOKLOG dispatch log, px9k89 was completed. However the planner cards predate that completion — no stale reference, just documentation lag.

## Recommendation

**REVIEW** — No critical security patterns found. The codebase demonstrates strong engineering discipline: thorough TDD, multi-platform parity, structured code review processes, and explicit input validation on all external data paths. The security concerns are medium severity and largely stem from structural patterns (bash-to-PowerShell variable interpolation, registry-controlled download paths) rather than explicit vulnerabilities.

The `peon-ping-config` skill's `user_invocable: false` / CLAUDE.md contradiction is the highest-priority bug for a PR, as it directly affects user experience. The `skills/peon-ping-log/SKILL.md` hardcoded path bug would silently fail for non-standard Claude config directory users.

The pack download mechanism (registry → manifest → sounds) represents the widest attack surface: a compromised GitHub Pages registry or a malicious pack publisher could substitute download sources. The existing input validation is a meaningful mitigation but not a complete defense. This warrants documenting the trust model in a security note in README.md or CONTRIBUTING.md.

Recommend: proceed with contribution for bugs #2 and #3 (skill bugs). Skip security medium findings from PR as they require design discussion. No blockers for contribution.
