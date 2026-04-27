# Audit: eroslifestyle/Claude-Orchestrator-Plugin

**Audited:** 2026-04-27  
**Commit:** unknown (target-repo clone without .git)  
**Auditor:** NLPM auditor v1 (manual)  
**Repo:** https://github.com/eroslifestyle/Claude-Orchestrator-Plugin

---

## NL Score Summary

**Overall score: 72 / 100**

| Category | Files | Avg Score | Key Penalty |
|----------|-------|-----------|-------------|
| Core agents (6) | orchestrator, analyzer, coder, reviewer, documenter, system_coordinator | 75 | Missing `model` in frontmatter on 4/6 files (-5 each); zero examples in 4/6 files (-15 each) |
| L1 Expert agents (22) | gui-super, database, security, mql, trading, tester, architect, integration, devops, languages, ai_integration, claude_systems, mobile, n8n, social_identity, offensive_security, reverse_engineering, mql_decompilation, browser_automation, mcp_integration, notification, payment_integration | 75 | Missing `model` in frontmatter on all 22 (-5 each); output format delegated to PROTOCOL.md reference |
| L2 Sub-agents (15) | gui-layout, db-query, security-auth, api-endpoint, test-unit, mql-optimization, trading-risk, mobile-ui, n8n-workflow, claude-prompt, architect-design, devops-pipeline, languages-refactor, ai-model, social-oauth | 70 | Minimal content beyond frontmatter; zero examples (-15 each); no output format (-10 each) |
| System docs (9) | AGENT_REGISTRY, COMMUNICATION_HUB, PROTOCOL, TASK_TRACKER, DEPENDENCY_GRAPH, PARALLEL_COORDINATOR, TASK_DECOMPOSITION, COMPLETION_NOTIFIER, METRICS_TRACKER | 75 | Non-agent docs; no model/examples penalty but missing structured output sections |
| Config (2) | routing.md, standards.md | 80 | Well-formed tables; minor vague quantifiers |
| Docs (17) | README, SYSTEM_ARCHITECTURE, INTEGRATION_REPORT, quickstart, getting-started, quick-reference, prompt-library, implementation-details, deploy-checklist, changelog, orchestrator-examples, orchestrator-advanced, DOCUMENTATION_STATUS, COMPLETION_REPORT, README_DOCUMENTATION, TODOLIST, DOCUMENTATION_INDEX | 65 | Broken refs in 2 files; stale counts in 2 files; missing output formats throughout |
| Tests (1) | routing-validation.md | 75 | Complete 50-entry routing table; minor format gaps |

**Scoring method:** Start at 100, apply deterministic penalties per artifact. Missing `model` in frontmatter: -5. Zero example blocks: -15. Only one example block: -5. Missing output format: -10. Vague quantifiers: -2 each (cap -20). Multi-step commands without numbered steps: -10.

**Files scanned:** ~72 NL artifacts across `github-package/agents/`, `agents/`, and associated skill/config files.

---

## Security Scan

### CRITICAL

None.

### HIGH

**H1 — `plugins/orchestrator-plugin/.mcp.json` line 4 — Hardcoded developer machine path**  
The MCP server configuration hard-codes an absolute Windows path: `c:\Users\LeoDg\.claude\plugins\orchestrator-plugin\mcp_server\server.py`. Every user who installs the plugin via `install.sh` will receive this `.mcp.json` via `git clone`, causing the MCP server to fail to start on any machine that is not the developer's own. This is a functional breakage on all target installs, and if the developer path were attacker-controlled, it would also be a privilege-escalation vector.  
**Pattern:** `hardcoded-absolute-path`  
**Rule:** SEC-hardcoded-path

**H2 — `plugins/orchestrator-plugin/install.sh` line 50 — curl-pipe-sh for UV installer**  
Step 2 of the install script executes `curl -LsSf https://astral.sh/uv/install.sh | sh`. This is a classic curl-pipe-sh pattern: the downloaded script is executed immediately without integrity verification (no checksum, no signature). A compromised or MitM'd CDN response would execute arbitrary code with user privileges at install time.  
**Pattern:** `curl-pipe-sh`  
**Rule:** SEC-curl-pipe-sh

**H3 — `github-package/agents/experts/mql_decompilation_expert.md` — License bypass instructions**  
The agent file contains explicit instructions for bypassing MetaTrader EA software protections: account number validation bypass, HWID fingerprinting bypass, trial/expiry checks removal, broker restriction removal, and demo-mode bypass. It references commercial decompilation tools (`EX4-TO-MQL`) and disassemblers (`IDA Pro`, `Ghidra`, `x64dbg`, `OllyDbg`) in the context of copy-protection circumvention. Distributing these instructions in a public plugin enables DMCA-violating or legally-risky usage at scale.  
**Pattern:** `license-bypass-instructions`  
**Rule:** SEC-license-bypass

**H4 — `github-package/agents/experts/offensive_security_expert.md` — C2 framework and EDR bypass references**  
The agent file contains working references to Cobalt Strike, Sliver C2, and explicit EDR/AV bypass techniques. While the file contextualizes this as "authorized red team operations," distributing an AI agent configured to provide detailed offensive toolchain guidance (C2 staging, shellcode writing, EDR bypass) in a public plugin exposes the plugin to misuse by unauthenticated end users without any authorization gate.  
**Pattern:** `c2-edr-bypass-instructions`  
**Rule:** SEC-offensive-tool-ref

### MEDIUM

**M1 — `plugins/orchestrator-plugin/mcp_server/server.py` line 744 — subprocess shell=True**  
`cleanup_orphan_processes()` calls `subprocess.run(cmd, shell=True, capture_output=True, timeout=5)` where `cmd` is a hardcoded string on Windows (`taskkill /F /IM python.exe /FI ...`) or Linux (`pkill -f '...'`). The command string is not user-influenced here, but shell=True widens the attack surface: if `cmd` were ever interpolated with user input, it would be a command injection. Best practice is shell=False with a list argument.  
**Pattern:** `subprocess-shell-true`  
**Rule:** SEC-shell-true

**M2 — `plugins/orchestrator-plugin/package.json` line 61 — postinstall script**  
`"postinstall": "npm run build"` runs `tsc && npm run copy-assets` automatically on `npm install`. The `scripts/` and `src/` TypeScript directories are included in the package, so `postinstall` is a code-execution hook on install. While the current content is benign (TypeScript compilation), this is a known attack vector: dependency confusion, supply-chain compromise, or a malicious version bump can execute arbitrary code on every developer machine that runs `npm install`.  
**Pattern:** `postinstall-build`  
**Rule:** SEC-postinstall-script

**M3 — `github-package/agents/CLAUDE.md` and `agents/CLAUDE.md` — Mandatory taskkill all processes**  
Both top-level CLAUDE.md files instruct Claude to execute `taskkill /F /IM python.exe`, `taskkill /F /IM node.exe`, `taskkill /F /IM bash.exe`, `taskkill /F /IM git.exe`, and others "at the end of EVERY task." The NUL KILLER V2.0 block uses Python `ctypes.windll.kernel32.DeleteFileW` via a one-liner. Embedding mandatory OS-level process termination commands in AI system prompts means Claude will routinely kill all Python and Node processes—regardless of whether those processes belong to the plugin or to unrelated user work.  
**Pattern:** `taskkill-all-processes`  
**Rule:** SEC-windows-process-kill

### LOW

No additional low-severity findings beyond what is noted in the bug section.

---

## Bugs

**BUG-1 (HIGH) — `plugins/orchestrator-plugin/.mcp.json` line 4 — Developer machine path makes MCP server non-functional**  
As described in H1 above. Every user who clones the repo gets a `.mcp.json` pointing to `c:\Users\LeoDg\.claude\...` which does not exist on their machine. The MCP server fails to start. The install.sh script overwrites this file during setup (Step 5 configures `settings.local.json` to reference it), but the shipped `.mcp.json` is the broken default state.  
**Fix:** Replace with a relative path or a generated path computed at install time.

**BUG-2 (HIGH) — `agents/docs/getting-started.md` — References to non-existent expert files**  
The file references `experts/iam_expert.md` and `experts/api_expert.md`. Neither file exists in the current repository. These were renamed/restructured in earlier versions: `iam_expert` was merged into `security_unified_expert.md`, and `api_expert` was merged into `integration_expert.md`.  
**Fix:** Update references to `experts/security_unified_expert.md` and `experts/integration_expert.md`.

**BUG-3 (HIGH) — `github-package/agents/docs/quick-reference.md` — Five stale expert file references**  
The quick reference document links to: `experts/api_expert.md`, `experts/mql5_expert.md`, `experts/pyqt5_expert.md`, `experts/python_expert.md`, and `experts/iam_expert.md`. None of these files exist. The replacements are: `integration_expert.md`, `mql_expert.md`, `gui-super-expert.md`, `languages_expert.md`, and `security_unified_expert.md`.  
**Fix:** Update all five path references.

**BUG-4 (LOW) — `github-package/agents/CLAUDE.md` header — Agent count off by one**  
The header section reads "44 Totali" but the footer and math both say 43 (6 L0 + 22 L1 + 15 L2 = 43). The routing table in `github-package/agents/core/orchestrator.md` confirms 43. This appears to be a copy-paste error from an earlier version.  
**Fix:** Change "44 Totali" to "43 Totali" in the header.

**BUG-5 (LOW) — `plugins/orchestrator-plugin/mcp_server/server.py` line 15 — Stale agent count in server**  
The module docstring says "Total Agents: 36 (6 Core + 15 L1 Expert + 15 L2 Sub-Agent)" and `handle_read_resource` returns `"total_agents": 36`. The actual deployed agent count is 43 (6 + 22 + 15). The server's agent list constant `KEYWORD_TO_EXPERT_MAPPING` maps keywords for 15 L1 experts (not 22), meaning 7 recently-added experts (browser_automation, mcp_integration, notification, payment_integration, reverse_engineering, offensive_security, mql_decompilation) are not reachable via the MCP server's keyword routing—only via the markdown orchestrator's routing table.  
**Fix:** Add the 7 missing experts to `KEYWORD_TO_EXPERT_MAPPING` and update the count to 43.

---

## Security Fixes

Priority order for security remediation:

1. **Replace `.mcp.json` hardcoded path** (H1): Generate the path dynamically in `install.sh` using `$ORCHESTRATOR_DIR/mcp_server/server.py`, or use a relative path with a wrapper script. This unblocks all non-developer installs.

2. **Remove or gate the offensive agent files** (H3, H4): `mql_decompilation_expert.md` and `offensive_security_expert.md` should either be removed from the public distribution or gated with explicit user acknowledgment (e.g., an opt-in install flag). The license-bypass instructions in the MQL decompilation expert are the highest-risk item for legal exposure.

3. **Replace curl-pipe-sh in install.sh** (H2): Download `astral.sh/uv/install.sh` to a temp file, verify its SHA256 against the published checksum, then execute. Or use the officially documented pinned install method with `--version`.

4. **Replace shell=True in MCP server** (M1): Use `subprocess.run(["taskkill", "/F", "/IM", "python.exe", ...], shell=False)` on Windows and the equivalent list form on Linux.

5. **Remove or scope the taskkill CLAUDE.md instructions** (M3): Limit the cleanup rules to processes that were explicitly spawned by the plugin, not all python/node/bash/git processes system-wide. Consider using the `ProcessManager` job-object pattern already implemented in `lib/process_manager.py` instead of blanket `taskkill`.

6. **Gate the postinstall script** (M2): Replace `"postinstall": "npm run build"` with a safe no-op or remove it; move the build step to a documented explicit `npm run build` command users run after cloning.

---

## Quality Issues

**Q1 — Missing `model` in frontmatter across ~35 of 43 agent files**  
Only `core/orchestrator.md` (v11.3) and `core/documenter.md` (v4.1) declare a model in frontmatter. All other core agents (analyzer, coder, reviewer, system_coordinator) and all 22 L1 experts and 15 L2 sub-agents omit it. Claude Code relies on this declaration to select the model at dispatch time. The routing tables in the markdown files and in `server.py` do specify models inline, but frontmatter is the authoritative source.  
**Affected penalty:** -5 per file × 35 files = -175 points total across the corpus.

**Q2 — Copy-paste taskkill boilerplate in every core agent file**  
The same 6-line `taskkill` + `rm -f ~/.claude/nul` block is copy-pasted into analyzer.md, coder.md, reviewer.md, system_coordinator.md, and several expert files. This creates maintenance burden: when the cleanup rule changes, every copy must be updated. The system already has `lib/process_manager.py` and a `system_coordinator` agent for resource management—the cleanup rule should live in one place (CLAUDE.md or system_coordinator.md) and be referenced, not repeated.

**Q3 — Version drift across core agent files**  
Core agents (analyzer, coder, reviewer) show "Versione: 6.2 - SISTEMA MULTI-AGENT V6.2" in their body headers while `CLAUDE.md` declares V12.0, `orchestrator.md` is V11.3, and `documenter.md` is V4.1. No single version scheme applies consistently. Users and automated tools cannot determine which version of any given agent is current.

**Q4 — L2 sub-agents have minimal content (zero examples)**  
All 15 L2 sub-agents contain only frontmatter (name, description) and a few lines of context. None have example blocks, output format specifications, or operational guidance beyond their two-line descriptions. This means Claude receives no behavioral anchoring when dispatched as an L2 specialist.  
**Penalty:** -15 per file (zero examples) × 15 files = -225 points total.

**Q5 — INTEGRATION_REPORT.md is severely stale**  
`github-package/agents/docs/INTEGRATION_REPORT.md` documents 11 experts with a V5.1 integration report, while the actual system has 22 L1 experts. The report's architecture diagram and integration metrics are ~50% behind reality.

---

## Cross-Component

**CC-1 — Agent count inconsistency across four locations**  
Four different files give four different agent counts:
- `github-package/agents/CLAUDE.md` header: 44
- `github-package/agents/CLAUDE.md` footer: 43
- `plugins/orchestrator-plugin/mcp_server/server.py` comment + resource: 36
- `github-package/agents/core/orchestrator.md` routing section: 43

The canonical count (6+22+15=43) is correct in `orchestrator.md` and the CLAUDE.md footer. The header (44) and MCP server (36) are wrong.

**CC-2 — MCP server keyword map covers only 15 of 22 L1 experts**  
`KEYWORD_TO_EXPERT_MAPPING` in `server.py` contains entries for the original 15 L1 experts but is missing the 7 experts added in later versions: `reverse_engineering_expert`, `offensive_security_expert`, `mql_decompilation_expert`, `browser_automation_expert`, `mcp_integration_expert`, `notification_expert`, and `payment_integration_expert`. Users accessing the system via MCP tools cannot reach these agents via keyword routing; they are only accessible if the user invokes the markdown orchestrator directly.

**CC-3 — Installer overwrites settings.local.json without JSON merging**  
`plugins/orchestrator-plugin/install.sh` lines 108–118 detect an existing `settings.local.json` but reconstruct it from scratch if `"orchestrator"` is not present, discarding existing keys. Users who have other MCP servers or custom settings configured will lose them silently.

**CC-4 — `skills/orchestrator/install.sh` is a separate installer with version 10.2 while the plugin installer is version 2.1.0**  
Two install scripts exist at different paths with different version numbers and potentially different logic. It is unclear which one is authoritative.

---

## Recommendation

**Ship-blocking issues (fix before public distribution):**
- BUG-1 / H1: `.mcp.json` hardcoded path breaks all installs
- H3: License-bypass content in `mql_decompilation_expert.md` — remove or add explicit opt-in gate
- BUG-2 / BUG-3: Broken agent file references in two doc files

**High-priority but non-blocking:**
- H4: Offensive security expert should have an authorization disclaimer or opt-in gate
- H2: curl-pipe-sh in installer (accepted risk but should be documented)
- BUG-5: MCP server missing 7 experts from keyword map (silent failure)

**Quality debt (can ship, fix soon):**
- Q1: Add `model` to frontmatter of all 35 agent files
- Q2: Consolidate taskkill boilerplate
- Q3: Establish a single version scheme
- Q4: Add examples to all 15 L2 sub-agents
- CC-1: Fix agent count discrepancy in 2 locations

The core architecture is sound: hub-and-spoke orchestration, clear separation of L0/L1/L2 responsibilities, PROTOCOL.md standardization, and circuit-breaker health management are all well-designed. The primary concerns are the hardcoded developer path that breaks every user install, the legally-sensitive MQL decompilation instructions, and the model-frontmatter gap that affects routing quality for 35 of 43 agents.
