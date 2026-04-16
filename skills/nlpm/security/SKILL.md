---
name: security
description: "Detects execution surface risks, supply chain vulnerabilities, data exfiltration vectors, and prompt injection patterns in Claude Code plugins. Use when auditing plugins for security risks, reviewing MCP server configurations, scanning hooks and scripts for vulnerabilities, or checking extensions before installation."
version: 0.1.0
---

# Security Scan Patterns for Claude Code Plugins

## Context-Aware File Classification

Before assigning severity to any finding, classify the file by its execution context:

| File Type | Examples | Can Execute? | Rule |
|-----------|----------|--------------|------|
| Shell scripts | `*.sh`, `*.bash` | Yes | Apply full severity table |
| Code files | `*.py`, `*.js`, `*.mjs`, `*.ts` | Yes | Apply full severity table |
| Hook definitions | `hooks/hooks.json` | Runs on every tool call | Apply full severity table |
| MCP configs | `.mcp.json` | Yes (server launch) | Apply full severity table |
| Package manifests | `package.json` | Via npm scripts | Apply full severity table |
| Documentation | `*.md` (SKILL.md, CLAUDE.md, README.md) | **No** | Cap at Low — see rule below |

### Documentation Files (*.md)

Patterns in `.md` files are instructional content, not executable code. A `curl | bash` in a README documents a user action the reader types manually — the plugin never runs it. Apply this rule universally:

**Any Critical or High pattern found in a `.md` file → downgrade to Low (informational).** Note it as "instructional content in documentation — not executable."

Examples:
- `curl https://... | bash` in README.md → Low: install instruction for end users
- `eval $var` in SKILL.md → Low: pattern shown as example to avoid
- `new Function(...)` in CLAUDE.md → Low: educational reference

Exception: if a `.md` file is explicitly referenced as a script via `command:` in `hooks.json` or executed via `bash file.md`, treat it as executable and apply full severity.

## Scanning Workflow

1. **Classify files** — categorize each file by execution context (see table above)
2. **Identify execution surfaces** — map hooks, scripts, MCP configs, commands, and install scripts
3. **Scan each surface** — apply pattern tables below, matching regex against file contents
4. **Apply context adjustments** — downgrade documentation findings to Low per the markdown rule
5. **Validate findings** — verify each Critical/High finding is in an executable context before finalizing
6. **Generate report** — produce the structured report (see Report Format section)

## Execution Surfaces

Claude Code plugins have five execution surfaces that must be scanned:

| Surface | Files | Risk Level | Why |
|---------|-------|------------|-----|
| Hooks | `hooks/hooks.json`, referenced scripts | Critical | Runs on EVERY tool call automatically |
| Scripts | `scripts/*.sh`, `*.py`, `*.js` | High | Executed by commands/agents |
| MCP Servers | `.mcp.json` | High | Network access, data flow |
| Bash in commands | `commands/*.md` with Bash tool | Medium | Shell execution via Claude |
| Install scripts | `package.json` postinstall, setup scripts | Medium | Runs on install |

## Dangerous Shell Patterns

### Critical (immediate risk)

| Pattern | Regex | Why |
|---------|-------|-----|
| Pipe to shell | `curl.*\|.*sh`, `wget.*\|.*bash` | Remote code execution |
| Eval with variables | `eval\s+["']?\$` | Arbitrary code execution |
| Reverse shell | `bash\s+-i\s+>&`, `/dev/tcp/` | Backdoor |
| Base64 decode and exec | `base64.*\|.*sh`, `base64.*\|.*python` | Obfuscated execution |
| SSH key exfiltration | `cat.*\.ssh/`, `scp.*\.ssh/` | Key theft |
| Token exfiltration | Secrets like GITHUB_TOKEN or API keys sent to curl/wget | Credential theft |

### High (likely dangerous)

| Pattern | Regex | Why |
|---------|-------|-----|
| Subprocess with shell=True | `subprocess\.(call\|run\|Popen).*shell\s*=\s*True` | Unsanitized input reaches shell |
| OS system calls | `os\.system\(` | No argument escaping; full shell interpretation |
| Dynamic require/import | `require\(\s*\$`, `import\(\s*\$` | Attacker-controlled module path |
| new Function with dynamic string | `new Function\(` with string concatenation or template literal | Arbitrary code execution from string; often used to deserialize data that could be imported directly |
| File write outside repo | `> ~/`, `> /etc/`, `> /tmp/.*\.sh` | System modification |
| Sudo usage | `sudo\s+` | Privilege escalation |
| PATH modification | Appending to bashrc, zshrc, or profile | Persistent system modification |

### Medium (context-dependent)

| Pattern | Regex | Why |
|---------|-------|-----|
| Network calls | `curl\s+`, `wget\s+`, `fetch\(`, `requests\.(get\|post)` | Could exfiltrate repo data to external host |
| Environment access | `process\.env`, `os\.environ`, shell variable expansion | May leak tokens, keys, or secrets |
| File reads outside repo | Reading from home directory or system paths | Exposes credentials or configs outside project |
| Runtime package install | `npm install`, `pip install`, `gem install` | Unvetted dependency pulled at runtime |
| Shell exec functions | Functions that execute strings as shell commands | String-to-shell boundary; injection risk |

## MCP Configuration Risks

Scan `.mcp.json` for:

| Risk | Check | Severity |
|------|-------|----------|
| Remote servers | `url` field pointing to non-localhost | High |
| Unknown domains | Domain not in known-safe list | High |
| Broad permissions | `permissions` with wildcard or extensive list | Medium |
| File system access | Server with `fs` or `filesystem` capability | Medium |
| Shell access | Server with `shell` or execution capability | Critical |
| Missing auth | Remote server without `auth` field | High |

Known-safe MCP domains: `localhost`, `127.0.0.1`, `modelcontextprotocol.io`, `github.com`, `api.anthropic.com`

## Hook Safety Rules

Scan `hooks/hooks.json` for:

| Risk | Check | Severity |
|------|-------|----------|
| Hook runs shell script | `command` field references `.sh`, `.py`, `.js` | Medium (must scan the script) |
| Hook uses user input | Script receives prompt or input variables without sanitization | High |
| Hook on every event | Triggers on PreToolUse or PostToolUse without tool filter | Medium |
| Hook modifies files | Script writes to disk on every tool call | Medium |
| Hook makes network calls | Script contains network request commands | High |

## Dependency Supply Chain

Scan `package.json` for:

| Risk | Check | Severity |
|------|-------|----------|
| postinstall scripts | `scripts.postinstall` exists | High |
| preinstall scripts | `scripts.preinstall` exists | High |
| Git URL dependencies | Deps pointing to git URLs | Medium |
| Unpinned versions | Wildcard or "latest" version (suppress if lockfile present: package-lock.json, bun.lock, yarn.lock, pnpm-lock.yaml) | Medium |

Scan `requirements.txt` / `pyproject.toml` for:

| Risk | Check | Severity |
|------|-------|----------|
| Git URL deps | git+https or git+ssh URLs | Medium |
| Unpinned | No version pin | Low |
| Direct URL | HTTP download URLs | High |

## Prompt Injection Surfaces

| Risk | Check | Severity |
|------|-------|----------|
| Untrusted file content in prompts | Agent reads arbitrary file then uses content in Bash | High |
| User input passed to shell | Command takes arguments and passes to Bash without sanitization | Critical |
| Template expansion | Variable expansion in hook scripts with user-controlled values | High |

## Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| Critical | Immediate exploitation risk: RCE, credential theft, backdoor | Block contribution, file security issue |
| High | Likely dangerous: shell injection, data exfil, privilege escalation | Block contribution, report in audit |
| Medium | Context-dependent: network calls, env access, runtime installs | Report in audit, flag for review |
| Low | Minor concern: unpinned deps, broad permissions | Report as informational |

## Finding Validation

Before finalizing findings, verify each Critical or High result:
- Confirm the file is in an executable context (not documentation)
- Check if the pattern is inside a comment, string literal, or example block
- Verify the pattern is reachable at runtime (not dead code behind a feature flag)
- Cross-reference with the project's test suite — a pattern in test fixtures is lower risk

## Report Format

The security scan section in an audit report follows this structure:

```
## Security Scan

| Severity | Count |
|----------|-------|
| Critical | N |
| High | N |
| Medium | N |
| Low | N |

### Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
```

## Risk Gate

If any Critical or High findings exist, the `contribute-approved` label must NOT be applied. The audit report must include a prominent warning and the tracking issue must link to the security findings.
