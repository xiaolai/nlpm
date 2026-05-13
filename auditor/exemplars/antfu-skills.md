---
slug: antfu-skills
repo: antfu/skills
audited: 2026-05-13
commit_sha: c35a5588a5158b5b404a14fb10469b2b6dc1952b
score: 93
exemplifies:
  - R04
  - R05
  - R06
  - R08
---

# Exemplar: antfu/skills

**Score**: 93/100  |  **Date**: 2026-05-13  |  **Commit**: `c35a5588a5158b5b404a14fb10469b2b6dc1952b`

A 17-skill collection for the Vue/Vite/Slidev ecosystem, notable for packing every description with specific trigger phrases and keeping three of the top skills under 200 lines each through a thin-index + deep-references architecture.

## Per-rule evidence

### R04 — Description as trigger

All three 100-point skills open with descriptions that enumerate distinct user queries rather than summarizing the tool. Each description puts the trigger phrase ("Use when...") before the taxonomy clause, matching the pattern a real user would type.

> `skills/slidev/SKILL.md:3`:
>
> ```
> description: Create and present web-based slidedecks for developers using Slidev with Markdown, Vue components, code highlighting, animations, and interactive features. Use when building technical presentations, conference talks, code walkthroughs, teaching materials, or developer decks.
> ```

> `skills/vite/SKILL.md:3`:
>
> ```
> description: Vite build tool configuration, plugin API, SSR, and Vite 8 Rolldown migration. Use when working with Vite projects, vite.config.ts, Vite plugins, or building libraries/SSR apps with Vite.
> ```

> `skills/vue/SKILL.md:3`:
>
> ```
> description: Vue 3 Composition API, script setup macros, reactivity system, and built-in components. Use when writing Vue SFCs, defineProps/defineEmits/defineModel, watchers, or using Transition/Teleport/Suspense/KeepAlive.
> ```

What makes these strong: each description packs 3–5 concrete scenario phrases a user would actually type — "vite.config.ts", "defineModel", "conference talks" — rather than abstract nouns like "a comprehensive Vite guide." A weaker description would read "Vue 3 best practices for component development."

---

### R05 — Body length

The three perfect-score skills use a thin-index architecture: the SKILL.md holds only a runnable quick-reference block plus a reference table of sub-files, delegating all deep content to `references/*.md`. This keeps the index files at 73–190 lines.

| Skill | Lines |
|-------|-------|
| `skills/vite/SKILL.md` | 73 |
| `skills/vue/SKILL.md` | 85 |
| `skills/antfu/SKILL.md` | 131 |
| `skills/slidev/SKILL.md` | 190 |
| `skills/turborepo/SKILL.md` | 912 ❌ |

The vite skill's reference table illustrates the pattern:

> `skills/vite/SKILL.md:22-34`:
>
> ```
> | Topic | Description | Reference |
> |-------|-------------|-----------|
> | Configuration | `vite.config.ts`, `defineConfig`, conditional configs, `loadEnv` | [core-config](references/core-config.md) |
> | Features | `import.meta.glob`, asset queries (`?raw`, `?url`), `import.meta.env`, HMR API | [core-features](references/core-features.md) |
> | Plugin API | Vite-specific hooks, virtual modules, plugin ordering | [core-plugin-api](references/core-plugin-api.md) |
> ```

Each table row describes what the sub-file covers in concrete API terms, so the main SKILL.md is an O(1) routing layer rather than a full content dump. The turborepo skill (912 lines, -10 penalty) shows what happens when this pattern is skipped.

---

### R06 — Runnable code examples

Both the vite and vue 100-point skills include complete, syntactically valid code blocks in the SKILL.md index — not pseudocode, not CLI flag lists, but copy-paste-ready artifacts.

The vue skill embeds a full component template covering `defineProps`, `defineEmits`, `defineModel`, `computed`, `watch`, and `onMounted` in a single block:

> `skills/vue/SKILL.md:38-68`:
>
> ```vue
> <script setup lang="ts">
> import { ref, computed, watch, onMounted } from 'vue'
>
> const props = defineProps<{
>   title: string
>   count?: number
> }>()
>
> const emit = defineEmits<{
>   update: [value: string]
> }>()
>
> const model = defineModel<string>()
>
> const doubled = computed(() => (props.count ?? 0) * 2)
>
> watch(() => props.title, (newVal) => {
>   console.log('Title changed:', newVal)
> })
>
> onMounted(() => {
>   console.log('Component mounted')
> })
> </script>
>
> <template>
>   <div>{{ title }} - {{ doubled }}</div>
> </template>
> ```

The vite skill pairs a runnable CLI block with a minimal but complete `defineConfig` snippet:

> `skills/vite/SKILL.md:46-64`:
>
> ```bash
> vite              # Start dev server
> vite build        # Production build
> vite preview      # Preview production build
> vite build --ssr  # SSR build
> ```
>
> ```ts
> import { defineConfig } from 'vite'
>
> export default defineConfig({
>   plugins: [],
>   resolve: { alias: { '@': '/src' } },
>   server: { port: 3000, proxy: { '/api': 'http://localhost:8080' } },
>   build: { target: 'esnext', outDir: 'dist' },
> })
> ```

What makes the vue example particularly strong: it isn't an isolated snippet for one API — it shows all the macros coexisting in a realistic component, the pattern an agent would need to answer "how do I use defineModel together with defineProps?"

---

### R08 — Patterns over theory

The antfu and vue skills state preferences as imperative patterns with explicit alternatives, not abstract principles. The antfu skill's testing section names the concrete decision in each line:

> `skills/antfu/SKILL.md:38-43`:
>
> ```
> - Test files: `foo.ts` → `foo.test.ts` (same directory)
> - Use `describe`/`it` API (not `test`)
> - Use `toMatchSnapshot` for complex outputs
> - Use `toMatchFileSnapshot` with explicit path for language-specific snapshots
> ```

The vue skill's preferences section leads with performance-relevant heuristics, not general philosophy:

> `skills/vue/SKILL.md:17-21`:
>
> ```
> - Prefer TypeScript over JavaScript
> - Prefer `<script setup lang="ts">` over `<script>`
> - For performance, prefer `shallowRef` over `ref` if deep reactivity is not needed
> - Always use Composition API over Options API
> - Discourage using Reactive Props Destructure
> ```

Each line names what to do AND the narrower case where it applies ("if deep reactivity is not needed"). Compare to a theory-first alternative: "Vue performance depends on choosing the right reactivity primitives" — true but untriggerable.

---

## Worth adopting

**Pattern: Thin-index + deep-references split.** A SKILL.md that serves as a routing layer (quick-start block + reference table with per-topic descriptions) delegates depth to `references/*.md` sub-files. This keeps context overhead under 200 lines for the common case while preserving full depth when the agent follows a reference link. Evidence: `skills/vite/SKILL.md` (73 lines) + `skills/vite/references/` (10 sub-files). Why it would be a useful rule: the 500-line budget in R05 is often violated not from negligence but from having no natural split point; this pattern provides one.

**Pattern: Inline verification step after quick-start commands.** The slidev skill adds a "Verify:" sentence after its build/run block, specifying what observable outcome confirms success. Evidence: `skills/slidev/SKILL.md:29` — "After `pnpm run dev`, confirm slides load at `http://localhost:3030`." Why it would be a useful rule: agents following quick-start instructions often stop after issuing commands; a verification clause closes the loop without adding a separate test section.
