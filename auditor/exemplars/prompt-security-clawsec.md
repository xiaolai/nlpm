---
slug: prompt-security-clawsec
repo: prompt-security/clawsec
audited: 2026-07-04
commit_sha: bc85af7203a20b369c470e6aeb5faf02d197e529
score: 99
exemplifies:
  - R04
  - R07
  - R06
  - R01
  - R33
  - R34
  - R38
---

# Exemplar: prompt-security/clawsec

**Score**: 99/100  |  **Date**: 2026-07-04  |  **Commit**: `bc85af7203a20b369c470e6aeb5faf02d197e529`

A 16-skill security-tooling collection (advisory feeds, guarded installers,
traffic monitors, drift detectors) spanning four agent harnesses
(OpenClaw, Hermes, NanoClaw, Picoclaw), with a project `CLAUDE.md` that
reads as an operations runbook rather than a description of the repo.

## Per-rule evidence

### R04 — Description is a trigger, not a summary

`skills/clawsec-nanoclaw/SKILL.md` packs three distinct trigger
conditions into a single `description` field instead of naming the
skill's category.

> Real quote from `skills/clawsec-nanoclaw/SKILL.md:4`:
>
> ```
> description: Use when checking for security vulnerabilities in NanoClaw skills, before installing new skills, or when asked about security advisories affecting the bot
> ```

This is the difference between a trigger and a label: "checking for
security vulnerabilities," "before installing new skills," and "asked
about security advisories" are three separate phrasings of real user
requests, each independently matchable, rather than one generic
"security skill for NanoClaw" tag.

### R07 — Scope note when related skills exist

The repo ships four near-identical `*-traffic-guardian` skills (Hermes,
NanoClaw, OpenClaw, Picoclaw) plus overlapping security-posture skills
(`clawsec-scanner`, `openclaw-audit-watchdog`, `soul-guardian`). Rather
than leaving the boundary implicit, `openclaw-traffic-guardian` states
it directly, by name:

> Real quote from `skills/openclaw-traffic-guardian/SKILL.md:105-117`:
>
> ```
> ## Scope
>
> Builders should use this skill as the OpenClaw landing zone for runtime traffic monitoring:
>
> - operator-scoped HTTP proxy inspection
> - optional HTTPS inspection with per-process CA trust
> - outbound exfiltration detection
> - inbound injection detection
> - approval-sensitive social-account mutation review
> - redacted local threat logs
> - optional OpenClaw hook/status integration
>
> Do not merge this capability into `clawsec-scanner`, `openclaw-audit-watchdog`, or `soul-guardian`. Those skills have different trust boundaries and safety contracts.
> ```

Naming the three specific sibling skills (not "related skills") is
what makes this actionable — an agent choosing between four security
skills has an explicit disambiguation rule instead of four similar
descriptions to guess between. `hermes-attestation-guardian` and
`nanoclaw-traffic-guardian` apply the same discipline in miniature:

> Real quote from `skills/hermes-attestation-guardian/SKILL.md:14-16`:
>
> ```
> IMPORTANT SCOPE:
> - This skill targets Hermes infrastructure only (CLI/Gateway/profile-managed deployments).
> - This skill is not an OpenClaw runtime hook package.
> ```

> Real quote from `skills/nanoclaw-traffic-guardian/SKILL.md:15`:
>
> ```
> This is a baseline specification skill. It intentionally does not ship a proxy or runtime implementation yet.
> ```

That second quote is a scope note pointed at the skill's own maturity,
not just at sibling skills — it tells the agent not to assume shipped
functionality that the name implies.

### R06 — Code examples must be runnable

Every skill that supports standalone (non-marketplace) install embeds
a complete, copy-pasteable release-verification script — not a
truncated snippet with a `# ...` in the middle.

> Real quote from `skills/hermes-attestation-guardian/SKILL.md:30-55`:
>
> ```bash
> set -euo pipefail
>
> SKILL_NAME="hermes-attestation-guardian"
> VERSION="0.1.6"
> REPO="prompt-security/clawsec"
> TAG="${SKILL_NAME}-v${VERSION}"
> BASE="https://github.com/${REPO}/releases/download/${TAG}"
> ZIP_NAME="${SKILL_NAME}-v${VERSION}.zip"
> TMP_DIR="$(mktemp -d)"
> trap 'rm -rf "$TMP_DIR"' EXIT
>
> RELEASE_PUBKEY_SHA256="711424e4535f84093fefb024cd1ca4ec87439e53907b305b79a631d5befba9c8"
>
> curl -fsSL "$BASE/checksums.json" -o "$TMP_DIR/checksums.json"
> curl -fsSL "$BASE/checksums.sig" -o "$TMP_DIR/checksums.sig"
> curl -fsSL "$BASE/signing-public.pem" -o "$TMP_DIR/signing-public.pem"
> curl -fsSL "$BASE/$ZIP_NAME" -o "$TMP_DIR/$ZIP_NAME"
> curl -fsSL "$BASE/SKILL.md" -o "$TMP_DIR/SKILL.md"
> curl -fsSL "$BASE/skill.json" -o "$TMP_DIR/skill.json"
>
> ACTUAL_PUBKEY_SHA256="$(openssl pkey -pubin -in "$TMP_DIR/signing-public.pem" -outform DER | shasum -a 256 | awk '{print $1}')"
> if [ "$ACTUAL_PUBKEY_SHA256" != "$RELEASE_PUBKEY_SHA256" ]; then
>   echo "ERROR: signing-public.pem fingerprint mismatch" >&2
>   exit 1
> fi
> ```

The script hardcodes the skill's own real version (`0.1.6`) and real
pinned public-key fingerprint rather than a `<VERSION>` placeholder —
an agent (or a human) can run it unmodified and get a pass/fail exit
code, which is what distinguishes a runnable example from illustrative
pseudocode.

### R01 — No vague quantifiers without criteria

`CLAUDE.md` states linter and rate-limit thresholds as exact numbers
instead of qualitative terms like "reasonable" or "strict":

> Real quote from `CLAUDE.md:111-116`:
>
> ```
> - **ESLint:** flat config (`eslint.config.js`), zero warnings policy
> - **Python:** ruff + bandit, configured in `pyproject.toml`, line-length 120
> - **Shell:** shellcheck on `scripts/*.sh`
> - **Tests:** each `.test.mjs` is a standalone Node.js script with its own pass/fail counters and `process.exit(1)` on failure. Tests generate ephemeral Ed25519 keys — they don't use the repo signing keys.
> - **Advisory feed:** fail-closed signature verification by default. `CLAWSEC_ALLOW_UNSIGNED_FEED=1` is a temporary migration bypass only.
> - **Hook event model:** hooks mutate `event.messages` array in-place (not return values). Rate-limited to 300s by default (`CLAWSEC_HOOK_INTERVAL_SECONDS`).
> ```

"Zero warnings," "line-length 120," and "300s" leave no room for the
agent to guess what "clean" or "rate-limited" means — each is a number
an agent (or CI) can check directly.

### R33 — Include build/run command

`CLAUDE.md` opens with the exact commands to get the frontend and
Python toolchain running, not a description of what the stack is.

> Real quote from `CLAUDE.md:5-19`:
>
> ```
> ## Development Setup
>
> \`\`\`bash
> npm install              # install JS dependencies
> npm run dev              # start Vite dev server on http://localhost:3000
> npm run build            # production build to dist/
> \`\`\`
>
> Python environment (use `uv`, not raw `pip`):
>
> \`\`\`bash
> uv venv                  # create .venv in repo root
> source .venv/bin/activate
> uv pip install ruff bandit   # linters configured in pyproject.toml
> \`\`\`
> ```

The `(use uv, not raw pip)` parenthetical is doing real work — it
forecloses the obvious wrong guess (`pip install`) instead of leaving
the agent to infer the convention from `pyproject.toml`.

### R34 — Include test command

Instead of "run the tests," `CLAUDE.md` lists the three actual test
file paths, because there is no `npm test` entry point to fall back on:

> Real quote from `CLAUDE.md:40-46`:
>
> ```
> **Tests** (vanilla Node.js — no framework, no npm test script):
>
> \`\`\`bash
> node skills/clawsec-suite/test/feed_verification.test.mjs
> node skills/clawsec-suite/test/guarded_install.test.mjs
> node skills/clawsec-suite/test/skill_catalog_discovery.test.mjs
> \`\`\`
> ```

The explicit `no npm test script` note matters as much as the
commands: without it, an agent would try `npm test`, get a missing-script
error, and have to discover the real invocation by reading `package.json`.

### R38 — More instructive than descriptive

The `Architecture` section of `CLAUDE.md` is one paragraph of prose
("Frontend: React 19 + TypeScript + Vite...") followed immediately by
enforceable, checkable facts about the skill-file contract:

> Real quote from `CLAUDE.md:83-86`:
>
> ```
> **Skills:** Each skill lives in `skills/<name>/` with:
> - `skill.json` — metadata, SBOM (file manifest), OpenClaw config (emoji, triggers, required bins)
> - `SKILL.md` — YAML frontmatter (`name`, `version`, `description`) + agent-readable markdown
> - Version in `skill.json` and `SKILL.md` frontmatter must match (CI enforced)
> ```

"Version ... must match (CI enforced)" is an instruction with a
built-in verification method, not a description of what the files
contain — an agent editing a skill's version now knows both what to do
and how it will be checked, in the same line.

## Worth adopting

Pattern: pin the release signing key's exact fingerprint inline in
every artifact that verifies it, not just in one canonical doc.
Evidence: `skills/hermes-attestation-guardian/SKILL.md:42`
(`RELEASE_PUBKEY_SHA256="711424e4535f84093fefb024cd1ca4ec87439e53907b305b79a631d5befba9c8"`)
and `CLAUDE.md:97` (`scripts/ci/verify_signing_key_consistency.sh`
enforces all references resolve to the same fingerprint, on every PR
and tag push). Why it would be a useful rule: an agent verifying a
signed artifact offline has no path to a canonical source of truth if
the fingerprint lives in only one file — inlining it everywhere it's
checked, with a CI drift guard that fails the build on mismatch, turns
a single-point-of-failure doc into a self-checking invariant.
