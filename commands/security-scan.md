---
name: security-scan
description: Scan a Claude Code plugin for security risks in executable artifacts (hooks, scripts, MCP configs, dependencies).
user-invocable: true
argument-hint: "[path]"
allowed-tools: Read, Glob, Grep, Task
---

# Security Scan

Scan a plugin or skill repo for security risks before auditing or contributing.

## Step 1: Parse Input

If arguments provided: use as target directory path.
If no arguments: use the current working directory.

Verify the target exists and contains at least one of:
- `.claude-plugin/`
- `agents/`
- `commands/`
- `skills/`
- `hooks/`
- `scripts/`

If none found: report "Not a Claude Code plugin directory" and stop.

## Step 2: Dispatch Security Scanner

Dispatch the `security-scanner` agent on the target directory.

Wait for the agent to complete and collect its report.

## Step 3: Present Results

Display the full report in this exact structure: the agent report as the body, followed by the gate banner as the footer. The `security-scanner` agent emits the body; this command appends only the banner.

```
{security-scanner agent report — verbatim}

────────────────────────────────────────────────────────────
{GATE BANNER — chosen per recommendation, see below}
────────────────────────────────────────────────────────────
```

Gate banners:

If the recommendation is BLOCK:
```
SECURITY GATE: BLOCKED
Critical/High security issues found. Do NOT install or contribute to this plugin without resolving these issues first.
```

If the recommendation is REVIEW:
```
SECURITY GATE: REVIEW NEEDED
Medium-severity findings detected. Review the findings before proceeding.
```

If the recommendation is PASS:
```
SECURITY GATE: PASSED
No Critical/High security issues found. Safe to proceed with audit and contribution.
```

**Error handling:**
- Target path does not exist → "Directory not found: {path}"
- `security-scanner` agent returns no report → "Security scan failed: no report produced. Re-run /nlpm:security-scan {path}."
