# NLPM for plugin authors

You're building a plugin or skill kit for Claude Code, Codex CLI, or Antigravity. NLPM checks one thing the official validators don't: **does your manifest match what's on disk?**

That single check has caught manifest-vs-disk bugs in plugins from authors with 16k-69k stars (see `analysis/ecosystem-gap.md`). The check is mechanical, fast, and runs without Claude Code installed — so it works the same whether you're shipping a `.claude-plugin/plugin.json`, a `.codex-plugin/plugin.json`, or an open-spec `SKILL.md` collection.

## The two surfaces

| Surface | What it does | When to use |
|---|---|---|
| **`bin/nlpm-check`** (standalone Python script) | Deterministic checks — manifest-vs-disk, frontmatter, hook event-name case — exits non-zero on findings | Pre-commit hooks, CI, pre-publish scripts |
| **`/nlpm:check` and `/nlpm:score`** (Claude Code slash commands) | Full 100-point quality scoring with judgment-required findings (vague language, instruction quality, etc.) | Interactive review during development |

Both surfaces share the same rule registry. The binary is the deterministic subset; the slash commands are the full set.

## Multi-plugin monorepos (v0.8.5+)

If your repo contains **multiple** `.claude-plugin/plugin.json` files (e.g., a monorepo with sub-plugins under `plugins/`), nlpm-check auto-detects and runs each sub-plugin's checks in isolation:

```bash
nlpm-check /path/to/monorepo
# nlpm-check: 12 plugins · 11 clean · 0 high · 2 medium · 0 low (/path/to/monorepo)
```

The badge message reflects the aggregate state: `N plugins clean` (green), `N of M plugins fail` (red), or `N plugins · K advisory` (yellow). Per-sub-plugin findings are emitted in the `--json` output under a `plugins[]` array; the top-level `summary` aggregates counts.

Nested sub-plugins are excluded from their parent's checks — each is checked exactly once.

## What the binary catches

High-confidence findings (exit code 1):
- **manifest-disk-diff**: a path declared in `plugin.json` doesn't exist on disk, or a SKILL.md / agent / command exists on disk but isn't reachable from the manifest
- **frontmatter**: missing required `name` (skills, agents) or `description` (commands, skills, agents)
- **skill name parent**: SKILL.md `name:` field doesn't match its parent directory (silently breaks Claude Code's skill loader)
- **skill name format**: SKILL.md `name:` violates the open spec format (`^[a-z][a-z0-9-]{0,63}$`)
- **hook event case**: `pretooluse` instead of `PreToolUse` (the loader is case-sensitive and silently ignores wrong-case events)

Medium-confidence findings (exit code 1 only under `--strict`):
- **hook event-name**: unknown event name not in the documented event list

For full quality scoring (description quality, vague language, instruction clarity, etc.) run `/nlpm:score` inside Claude Code.

## Install the binary

The binary is a single Python 3.11+ file with no external dependencies.

```bash
# Option A — into /usr/local/bin
curl -fsSL -o /usr/local/bin/nlpm-check \
  https://raw.githubusercontent.com/xiaolai/nlpm/main/bin/nlpm-check
chmod +x /usr/local/bin/nlpm-check

# Option B — into your repo (commits the script alongside your code)
mkdir -p bin
curl -fsSL -o bin/nlpm-check \
  https://raw.githubusercontent.com/xiaolai/nlpm/main/bin/nlpm-check
chmod +x bin/nlpm-check
```

Verify:

```bash
nlpm-check --version
# nlpm-check 0.8.0
```

## Use it in your authoring workflow

### 1. Editing — slash command (in Claude Code)

While in Claude Code, run `/nlpm:check` to surface findings inline. The hook installed by the plugin emits advisory checks as you write SKILL.md / agent / command files.

### 2. Committing — pre-commit hook

Copy the template:

```bash
curl -fsSL -o .git/hooks/pre-commit \
  https://raw.githubusercontent.com/xiaolai/nlpm/main/templates/pre-commit-nlpm.sh
chmod +x .git/hooks/pre-commit
```

Now `git commit` blocks if NLPM finds high-confidence issues. Bypass with `git commit --no-verify` (not recommended).

If you use the [`pre-commit`](https://pre-commit.com/) framework, add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: nlpm-check
        name: nlpm-check
        entry: nlpm-check
        language: system
        pass_filenames: false
        files: '(\.claude-plugin/.+\.json|skills/.+/SKILL\.md|agents/.+\.md|commands/.+\.md|hooks/hooks\.json)$'
```

### 3. Pushing — GitHub Actions

Copy the workflow template:

```bash
mkdir -p .github/workflows
curl -fsSL -o .github/workflows/nlpm-check.yml \
  https://raw.githubusercontent.com/xiaolai/nlpm/main/templates/workflows/nlpm-check.yml
```

Commit. Every push and PR now runs `nlpm-check`. No secrets required.

### 4. Showing a "Validated by NLPM" badge

The GHA workflow template publishes `nlpm-badge.json` to the repo root on every push to `main`. Add this to your README:

```markdown
![Validated by NLPM](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/YOUR-USER/YOUR-REPO/main/nlpm-badge.json)
```

The badge auto-updates each push to `main`:

| State | Color | Message |
|---|---|---|
| Clean | green | `0 issues · v0.8.x` |
| Advisory | yellow | `0 high · N advisory` (medium/low findings only) |
| Failing | red | `N high issues` |

The JSON payload includes a `manifest_disk_consistent` boolean and the SHA-stamped `checked_at` timestamp under `extras` for downstream verification.

To run it manually (e.g., the first time, before CI catches up):

```bash
nlpm-check --json . | nlpm-badge > nlpm-badge.json
git add nlpm-badge.json
git commit -m "chore: add nlpm-badge.json"
```

### 5. Publishing — release script

Add to your publish script (npm publish, release-please, manual):

```bash
nlpm-check --strict . || {
  echo "nlpm-check found issues. Fix them or run /nlpm:fix in Claude Code."
  exit 1
}
```

`--strict` exits 1 on findings of any confidence (high + medium + low).

## What NLPM does NOT replace

NLPM is **complementary** to the official validators. Run both.

| Tool | What it covers |
|---|---|
| `claude plugin validate` (Anthropic, built-in) | Manifest JSON syntax + deprecation warnings |
| `plugin-validator` (Anthropic agent) | Per-component frontmatter, security checks, MCP configs |
| `skills-ref` (Linux Foundation) | Per-skill frontmatter validity, name conventions |
| **NLPM** | Cross-component consistency (manifest-vs-disk), hook event-name case, frontmatter |

If you can only adopt one validator: pick the one that covers your most likely failure mode. If you've been bitten by "I added a skill but users can't see it" — that's the manifest-vs-disk gap, and NLPM is the only tool that catches it.

## JSON output

For machine consumption:

```bash
nlpm-check --json .
```

```json
{
  "version": "0.8.0",
  "plugin_root": "/path/to/plugin",
  "findings": [
    {
      "confidence": "high",
      "rule": "manifest-disk-diff",
      "path": "skills/foo/SKILL.md",
      "line": 0,
      "message": "SKILL.md exists on disk but not registered by plugin.json `skills`",
      "fix": "Add `skills/foo/` to plugin.json `skills` array"
    }
  ],
  "summary": {"high": 1, "medium": 0, "low": 0}
}
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean (or `--strict` not set and no high-confidence findings) |
| 1 | One or more high-confidence findings (or any finding under `--strict`) |
| 2 | Error reading the manifest, path not found, etc. |

## Reporting issues

NLPM rules cite primary sources (Anthropic docs, the Agent Skills spec). If a check is wrong, file an issue with the docs URL that contradicts it: <https://github.com/xiaolai/nlpm/issues>.

## Vocabulary discipline (R51, opt-in)

NLPM ships a sixth rule — R51 — that flags **vocabulary drift**: the same concept named differently across artifacts ("scanner" / "analyzer" / "linter"; "score" / "grade" / "rate"). It is disabled by default. Adopt it when your project has accumulated enough drift to be worth disciplining; skip it when the project is small or still finding its terms.

The six principles behind R51 live in NLPM's `analysis/vocabulary-design-principles.md`. The short version:

1. One term per distinct identity, at uniform granularity, within a declared scope.
2. Nouns are rigid artifacts; verbs are state-changing acts.
3. A verb is top-level only if it gates or produces a named artifact.
4. The vocabulary is closed under its own operations within scope.
5. Comprehensive means no unnamed judgment.
6. A term requires warrant (literary, user, structural, or domain) before it enters.

### When to adopt

| Signal | Adopt? |
|--------|--------|
| Project has 10+ NL artifacts (commands, agents, skills, rules) | Yes — drift is likely |
| Multiple contributors with different terminology habits | Yes — controlled vocabulary pays off |
| Same concept appears under 2+ names in your corpus | Yes — R51 will find these |
| Project is <5 artifacts, single author, exploring | No — premature |
| You can't yet name your domain in a sentence | No — discover your vocabulary first |

### The four-step adoption flow

1. **Bootstrap.** Run `/nlpm:vocab-init` from your project root. It detects your layout, extracts literary warrant from your corpus, and seeds a `skills/<plugin>/vocabulary/` skill with the top extracted terms. Nothing enforced yet — just scaffolding.

2. **Prune and define.** Open `skills/<plugin>/vocabulary/SKILL.md` and `registry.yaml`. Most top-extracted terms are real; some are noise. Delete what's wrong, define `deprecated:` synonym lists for canonical terms, declare your scopes (P1).

3. **(Optional) Hunt for hidden drift.** Run `/nlpm:vocab-drift` against your project. It uses judgment-based clustering to surface candidate synonym pairs the deterministic extractor missed (different surface forms, contextual co-occurrence). The output is advisory — review and decide whether each pair is genuine drift or a real distinction.

4. **Opt in.** Add to `.claude/nlpm.local.md`:

   ```yaml
   rule_overrides:
     R51:
       enabled: true
       vocabulary_skill: skills/<plugin>/vocabulary/
   ```

   `/nlpm:score` now penalizes deprecated-synonym occurrences (-2 each, cap -10/file). `/nlpm:check` lists drift findings alongside reference-integrity issues.

### Worked example

A plugin author has been writing for six months. The corpus contains:

- `commands/lint.md` — body says "the linter scans your code"
- `commands/score.md` — body says "the scorer analyzes each file"
- `agents/analyzer.md` — agent named `analyzer`
- `docs/intro.md` — "use the validator to check your work"

Four terms (`lint`, `score`, `analyze`, `validate`) and three role-names (`linter`, `scorer`, `analyzer`, `validator`) for two underlying operations.

After `/nlpm:vocab-init`:

- `skills/myplugin/vocabulary/SKILL.md` lists all four verbs with `frequency` counts.
- The author decides: `score` is canonical for quantitative work; `check` is canonical for structural work; `lint`, `analyze`, `validate` become deprecated synonyms (each declared against the matching canonical).
- The author defines two scopes: `internal` (commands/agents/skills) and — if relevant — `external` (a CI integration directory).
- Author opts in via `.claude/nlpm.local.md`.

Subsequent `/nlpm:score` runs flag every `lint` / `analyze` / `validate` occurrence with the canonical-replacement suggestion. The corpus converges. New contributors hit the rule before they cement a new synonym into the codebase.

### Registry-free option: `/nlpm:vocab-drift`

If you don't want to maintain a registry but still want vocabulary feedback, run `/nlpm:vocab-drift` periodically. It scans the corpus, clusters near-synonyms, and reports candidate drift pairs without requiring a declared canonical. Output is advisory only — no penalty, no opt-in needed. Useful for early-stage projects that want a vocabulary health check without committing to enforcement.

### See also (vocabulary)

- NLPM's own `skills/nlpm/vocabulary/SKILL.md` — the reference implementation R51 was designed against.
- NLPM's `analysis/vocabulary-design-principles.md` — the six principles in full, with retirement criteria.
- The `/nlpm:vocab-init` and `/nlpm:vocab-drift` command source files for the precise workflow each runs.

---

## See also

- `analysis/ecosystem-gap.md` — why this validator exists and what other tools do
- `analysis/scope-expansion-2026-05.md` — the broader plan for author-facing NLPM
- `analysis/vocabulary-design-principles.md` — the six principles behind R51
- The full slash-command surface — install the plugin: `claude plugin install nlpm@xiaolai --scope project`
