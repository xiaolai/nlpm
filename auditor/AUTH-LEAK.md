# Auth-Leak Risk and Mitigation Status

## What this document covers

Four auditor workflows give Claude (via `claude-code-action`) the `Bash`
tool while reading content from arbitrary upstream repos. Any such content
could carry a prompt-injection payload that instructs Claude to exfiltrate
the workflow's token (`PAT_TOKEN`, `GITHUB_TOKEN`, or
`CLAUDE_CODE_OAUTH_TOKEN`) via a network channel.

This is a structural risk in the `claude-code-action` pattern, not a bug
in any specific workflow. See the discussion at v0.8.12 for the full
attack-surface analysis.

## Affected workflows

| Workflow | Token in env | What it reads from upstream |
|---|---|---|
| `auditor-classify.yml` | `CLAUDE_CODE_OAUTH_TOKEN` (auth only) | Maintainer dissent quotes mined into `disagreements.jsonl` |
| `auditor-case-study.yml` (write-article step) | `CLAUDE_CODE_OAUTH_TOKEN` | Target repo source files for the case study narrative |
| `auditor-refine-rules.yml` | `GITHUB_TOKEN` (this repo write) | Maintainer quotes + downstream suppression reasons |
| `auditor-contribute.yml` | **`PAT_TOKEN`** (cross-org write) | Target repo source files + audit findings — **highest blast radius** |

## Layer 1 — applied in v0.8.13

Every Bash-granting `claude-code-action` invocation now passes
`--disallowedTools` with explicit Bash-command denylist:

```
--disallowedTools "Bash(curl:*)" "Bash(wget:*)" "Bash(nc:*)" "Bash(ncat:*)"
                  "Bash(socat:*)" "Bash(telnet:*)" "Bash(ssh:*)" "Bash(scp:*)"
                  "Bash(sftp:*)" "Bash(rsync:*)" WebFetch WebSearch
```

This blocks the textbook exfiltration channels — direct HTTP POST,
file upload over SSH/SCP, raw socket relay via `nc`/`ncat`/`socat`,
and Claude's built-in `WebFetch` / `WebSearch` tools.

**What it does NOT block:**
- `python3 -c "...socket..."` — sophisticated attackers can pivot
  through a scripting runtime
- `git push <attacker-url>` — git is required for legitimate operation
- `gh repo create attacker/x --public` — gh is required for legitimate
  operation; could be subverted to push code to an attacker-controlled fork

This is **defense in depth, not a fix**. It raises the bar for
opportunistic / textbook-payload attackers; it does not defeat a
determined adversary.

## Layer 2 — queued, not yet applied

The structural fix is **patch-only LLM separation**:

1. LLM step gets no token, only read access to audit data
2. LLM produces a unified diff as an artifact (text on disk)
3. A second, deterministic shell step (no LLM) applies the diff and
   runs `git push` / `gh pr create` with the token

This eliminates the attack surface: the step that holds the token never
reads untrusted content; the step that reads untrusted content never
holds a token.

**Cost of doing it:** ~2-4 hours per workflow (contribute + refine-rules).
Requires:
- New prompt structure that produces parseable diff output
- New post-LLM step that validates and applies the diff
- Failure-recovery paths (what if Claude's diff doesn't apply?)
- Loss of some autonomy (Claude can't run `gh pr view` to check existing
  PRs — has to operate from a snapshot)

**Why not done yet:** layer 1 reduces immediate risk; layer 2 is the
correct fix but needs dedicated session time + integration test coverage
to avoid breaking the auditor cron during the rewrite.

## Operational practices that further reduce risk

1. **PAT rotation cadence.** PAT_TOKEN should be rotated regularly so
   any successful exfiltration has a bounded blast window. If rotation
   is event-driven ("when I remember"), the risk is materially higher
   than the static math suggests.

2. **Discovery filter quality.** The discover workflow filters target
   repos by star count (≥500) and artifact count, which raises the
   bar for an attacker to bootstrap a malicious target. A determined
   actor could still publish a plausible-looking plugin and wait for
   it to gain stars before adding injection — slow but possible.

3. **Out-of-band monitoring.** Watch for anomalous PR creation on
   xiaolai's other repos (anything outside `nlpm-for-claude`'s
   discovery list). If PAT_TOKEN is exfiltrated and used, this is
   where it would show up first.

## Status

| | Status |
|---|---|
| Layer 1 (denylist) | **Applied v0.8.13** to all 4 Bash-granting workflows |
| Layer 2 (patch-only) | Queued as dedicated session work |
| PAT rotation cadence | User-managed; not automated |
| Out-of-band monitoring | None currently; manual review of unfamiliar PRs |
| Observed exfiltration to date | None known (200+ repos audited) |
