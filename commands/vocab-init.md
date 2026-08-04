---
name: vocab-init
description: "Create a vocabulary skill for the target project — detect layout, extract literary warrant from the corpus, seed canonical noun/verb tables, write the opt-in stub. Use to start adopting R51 vocabulary discipline in any Claude Code plugin or NL-artifact-heavy repo."
argument-hint: "[path]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

## User Input

```text
$ARGUMENTS
```

## Workflow

### Step 1: Resolve target path

Parse `$ARGUMENTS`:

| Input | Behavior |
|-------|----------|
| (empty) | Target = current working directory |
| absolute path | Target = that path |
| relative path | Target = `<cwd>/<path>` |

If the target does not exist or is not a directory → "Target path not found: {path}". Stop.

### Step 2: Detect plugin name

Read `<target>/.claude-plugin/plugin.json` if it exists. Use the `name` field.

If no manifest exists, use the basename of the target directory (e.g., `/home/dev/my-project/` → `my-project`). Lowercase, replace spaces/underscores with hyphens.

Store as `plugin_name` for the rest of the workflow.

### Step 3: Detect layout

Use `Glob` against the target path to check which of these patterns exist; build the scope config from what is present:

| Pattern | Scope | Role | Notes |
|---------|-------|------|-------|
| `commands/*.md` | internal | verb-filename | Claude Code plugin commands |
| `agents/*.md` | internal | noun-filename | Claude Code plugin agents |
| `skills/*/*/SKILL.md` | internal | skill-dirname | Plugin-namespaced skills |
| `skills/*/SKILL.md` | internal | skill-dirname | Flat skill layout (no plugin namespace) |
| `.github/workflows/*.yml` | auditor | verb-filename | Auditor-style workflows; only emit this scope if at least 3 workflow files match `auditor-*` or similar pipeline naming |
| `hooks/hooks.json` | internal | (no extraction; presence-only) | Skip in scope config; just note in the skeleton |
| `docs/*.md` | internal | headings | Author/user docs |
| `analysis/*.md` | internal | headings | Design notes |

Only include scopes where at least one matching file exists. If only `docs/` matches and nothing else, the project has too little NL surface for vocabulary discipline — stop with: "Target has minimal NL surface (only {N} files matched). Vocabulary discipline is premature here. Re-run /nlpm:vocab-init after the artifact set grows."

### Step 4: Write the scope config

Create `<target>/analysis/vocab-init-scopes.json` with the detected scopes. Format:

```json
{
  "scopes": {
    "commands": { "scope": "internal", "glob": "commands/*.md", "role": "verb-filename" },
    "agents":   { "scope": "internal", "glob": "agents/*.md",   "role": "noun-filename" }
  }
}
```

Include only the scopes detected in Step 3.

### Step 5: Run the extractor

Find NLPM's plugin root. Two paths to try in order:

1. `${CLAUDE_PLUGIN_ROOT}/analysis/scripts/extract-vocabulary.py` — set when the command runs from within NLPM
2. Fall back to running the script via Bash with the literal path the user has NLPM installed at (probe `~/.claude/plugins/cache/xiaolai/nlpm/*/analysis/scripts/extract-vocabulary.py` with Glob)

Invoke via Bash:

```bash
python3 <nlpm-root>/analysis/scripts/extract-vocabulary.py \
  --root <target> \
  --scopes <target>/analysis/vocab-init-scopes.json \
  --out <target>/analysis/vocabulary-extract/
```

If the script exits non-zero, stop and report the stderr. Otherwise, the extraction wrote three files into `<target>/analysis/vocabulary-extract/`: `summary.md`, `verbs.json`, `nouns.json`.

### Step 6: Read the extraction output

Read `<target>/analysis/vocabulary-extract/verbs.json` and `nouns.json`. Extract:

- **Top verbs by total frequency**, partitioned by scope (`internal` / `auditor`). Cut off at frequency ≥ 2, max 15 per scope.
- **Top role-nouns** (from `agents:filename` source) — these become the implementation-role section.
- **Top concept-nouns** (from `skills:dirname` source) — these become artifact-class or domain nouns; adopter decides.
- **Top heading nouns** filtered to single-word repeated proper-cased terms with frequency ≥ 3.

### Step 7: Write `skills/<plugin>/vocabulary/SKILL.md` skeleton

Write to `<target>/skills/<plugin_name>/vocabulary/SKILL.md`. If the file already exists, stop with: "Vocabulary skill already exists at {path}. Refusing to overwrite. Re-run after backing up if you want to regenerate."

Use this template (substitute `{plugin_name}` and the extracted term tables):

```markdown
---
name: vocabulary
description: "Use when writing, reviewing, or naming any {plugin_name} artifact — pick the canonical noun or verb from this registry rather than coining a synonym. Loaded by NLPM's scorer and checker when R51 is enabled in .claude/nlpm.local.md."
version: 0.1.0
---

# {plugin_name} Domain Vocabulary

> The canonical noun-and-verb set for {plugin_name}. Every artifact name, prose description, and rule wording should draw from this registry. Synonyms are flagged by `/nlpm:check` and penalized by `/nlpm:score` when R51 is enabled.
>
> **Status:** seeded by `/nlpm:vocab-init` on {ISO date}. Adopter must prune, define deprecation pairs, and confirm scopes before enforcement. Re-run `analysis/scripts/extract-vocabulary.py` after artifact changes to refresh.

---

## Scopes (P1 of vocabulary-design-principles.md)

{For each detected scope, emit a row with its name, path-prefix, and a one-line description the adopter fills in.}

| Scope | Paths | Description |
|-------|-------|-------------|
| internal | commands/, agents/, skills/, ... | (fill in: what {plugin_name} does to its own artifacts) |
| auditor  | .github/workflows/, auditor/    | (only if detected) |

## Verbs (literary warrant from corpus)

{For each scope, emit a table of extracted verbs. Mark every `deprecated:` column as TODO — adopter fills in.}

### internal scope

| Canonical verb | Frequency | Deprecated synonyms (fill in) |
|----------------|-----------|------------------------------|
| `<verb1>` | <N> | (none yet) |
| `<verb2>` | <N> | (none yet) |

### auditor scope (omit if not detected)

| Canonical verb | Frequency | Deprecated synonyms (fill in) |
|----------------|-----------|------------------------------|

## Nouns (literary warrant from corpus)

### Artifact-class nouns
| Canonical | Frequency | Definition (fill in) |
|-----------|-----------|----------------------|
| `<noun1>` | <N> | |

### Role-nouns (agent names paired with their verbs)

| Role-noun | Paired verb (fill in) |
|-----------|----------------------|
| `<role1>` | `<verb>` |

---

## How to extend

1. Re-run extraction: `python3 <nlpm-root>/analysis/scripts/extract-vocabulary.py --root . --scopes analysis/vocab-init-scopes.json`
2. New terms appear in `analysis/vocabulary-extract/summary.md`.
3. Add a row to the right table above. Cite at least one file as evidence.
4. To deprecate a synonym, list it in the canonical term's "deprecated synonyms" column.

## Adopting R51

R51 is **off by default**. To enable vocabulary drift detection on this project, add to `.claude/nlpm.local.md`:

```yaml
rule_overrides:
  R51:
    enabled: true
    vocabulary_skill: skills/{plugin_name}/vocabulary/
```

Without this opt-in, R51 contributes zero penalty regardless of artifact contents.

## See also

- NLPM's own vocabulary skill (the template this was seeded from): `skills/nlpm/vocabulary/SKILL.md` in the NLPM repo
- The six principles: `analysis/vocabulary-design-principles.md` in the NLPM repo
```

### Step 8: Write `registry.yaml` stub

Write to `<target>/skills/<plugin_name>/vocabulary/registry.yaml`:

```yaml
# Machine-readable vocabulary registry for {plugin_name}.
#
# Seeded by /nlpm:vocab-init on {ISO date}. Adopter must prune and
# define deprecation pairs before R51 enforcement produces useful signal.
#
# Read by /nlpm:check and /nlpm:score when R51 is enabled in
# .claude/nlpm.local.md.

scopes:
  - id: internal
    description: (fill in)
    paths:
      - commands/
      - agents/
      - skills/

# Verbs that mean the same in both scopes. Add entries here for
# sanctioned cross-scope homonyms (e.g., "scan", "test", "discover" in
# NLPM). Until populated, every cross-scope occurrence will be flagged.
cross_scope_homonyms:
  verbs: []

verbs:
  internal:
    {one entry per top verb, each with empty deprecated:[]}

nouns:
  artifact_class:
    {one entry per top concept-noun, each with empty deprecated:[]}
  role_nouns:
    {one entry per top role-noun from agents:filename}

# Verbs proposed but rejected pending warrant. Use this section to
# record vocabulary requests that didn't earn entry — keeps PR
# discussions from re-proposing the same rejected term.
rejected_pending_warrant: []
```

Substitute the extracted top-N terms; leave every `deprecated:` array empty.

### Step 9: Print opt-in instructions

```
Vocabulary scaffolding generated for {plugin_name}.

  Skill: skills/{plugin_name}/vocabulary/SKILL.md   ({N} verbs, {M} nouns seeded)
  Registry: skills/{plugin_name}/vocabulary/registry.yaml
  Scope config: analysis/vocab-init-scopes.json
  Extraction output: analysis/vocabulary-extract/

Next steps:
  1. Prune the seeded tables. Most top-extracted terms are real, but headings can be noisy.
  2. Fill in deprecated synonyms for at least 3–5 canonical terms. Without deprecation pairs, R51 produces zero findings.
  3. (Optional) Run /nlpm:vocab-drift to find candidate synonym pairs the extractor didn't surface.
  4. Opt in by adding to .claude/nlpm.local.md:

       rule_overrides:
         R51:
           enabled: true
           vocabulary_skill: skills/{plugin_name}/vocabulary/

  5. Re-run /nlpm:score and /nlpm:check to see R51 findings.

Reference: see NLPM's analysis/vocabulary-design-principles.md for the six principles behind this discipline.
```

## Error Handling

| Condition | Response |
|-----------|----------|
| Target path doesn't exist | "Target path not found: {path}" |
| Target has minimal NL surface (only docs/ matched) | Premature-message from Step 3 |
| Vocabulary skill already exists at target | "Vocabulary skill already exists at {path}. Refusing to overwrite." |
| Extractor exits non-zero | "Extraction failed: {stderr}. Aborting bootstrap." |
| NLPM root not findable | "Could not locate NLPM's extract-vocabulary.py. Set CLAUDE_PLUGIN_ROOT or install NLPM at user scope." |
