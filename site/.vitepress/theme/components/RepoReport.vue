<!--
  RepoReport.vue — renders one RepoReportData (see report-data-schema.md).
  Same shape consumed by bin/nlpm-report's static HTML; here we render
  via Vue with VitePress theme tokens for light/dark adaptive coloring.

  Handles two extremes gracefully:
    - Clean 100/100 self-audit (NLPM) — most arrays empty; show a
      "clean" affirmative state.
    - Heavy external audit — populated findings, files, drift, etc.
-->
<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, computed } from 'vue'
import { Graph } from '@antv/g6'

type Finding = {
  rule: string
  severity: 'high' | 'medium' | 'low'
  confidence?: 'high' | 'medium' | 'low'
  file?: string
  line?: number | null
  message: string
}
type FileEntry = { path: string; type: string; score: number | null; findings: Finding[] }
type HistoryPoint = { timestamp: string; average_score: number; kind?: string }
type DriftCandidate = {
  terms: string[]
  confidence: string
  disposition: string
  suggested_canonical: string
  files_affected: number
  evidence?: string
}
type RepoMeta = {
  status?: string | null
  stars?: number | null
  security?: string | null
  audit_report_path?: string | null
}

type RepoReportData = {
  project: string
  generated_at?: string
  score_threshold?: number
  r51_enabled?: boolean
  summary: {
    total_files: number
    average_score: number | null
    pass_count: number
    fail_count: number
  }
  files: FileEntry[]
  history: HistoryPoint[]
  cross_component?: { nodes: any[]; edges: any[] }
  vocabulary?: any
  vocab_drift?: { candidates: DriftCandidate[] }
  findings: Finding[]
  repo_meta?: RepoMeta | null
}

const props = defineProps<{ data: RepoReportData }>()
const d = computed(() => props.data)

const scoreTone = computed(() => {
  const s = d.value.summary?.average_score
  if (s === null || s === undefined) return ''
  const t = d.value.score_threshold ?? 70
  return s >= t ? 'pass' : 'fail'
})

const findingsByRule = computed(() => {
  const groups: Record<string, Finding[]> = {}
  for (const f of d.value.findings || []) {
    const k = f.rule || 'UNCLASSIFIED'
    ;(groups[k] = groups[k] || []).push(f)
  }
  return Object.keys(groups).sort().map((k) => ({ rule: k, items: groups[k] }))
})

const isClean = computed(() => (d.value.findings?.length ?? 0) === 0)

// File table sort
const fileSortKey = ref<'path' | 'type' | 'score' | 'findings'>('score')
const fileSortDir = ref<'asc' | 'desc'>('asc')
const sortedFiles = computed(() => {
  const files = [...(d.value.files || [])]
  files.sort((a, b) => {
    if (fileSortKey.value === 'findings') {
      const av = a.findings.length, bv = b.findings.length
      return fileSortDir.value === 'asc' ? av - bv : bv - av
    }
    const av = a[fileSortKey.value]
    const bv = b[fileSortKey.value]
    if (typeof av === 'number' && typeof bv === 'number') {
      return fileSortDir.value === 'asc' ? av - bv : bv - av
    }
    const sa = String(av ?? ''), sb = String(bv ?? '')
    return fileSortDir.value === 'asc' ? sa.localeCompare(sb) : sb.localeCompare(sa)
  })
  return files
})
function sortFilesBy(k: 'path' | 'type' | 'score' | 'findings') {
  if (fileSortKey.value === k) fileSortDir.value = fileSortDir.value === 'asc' ? 'desc' : 'asc'
  else { fileSortKey.value = k; fileSortDir.value = k === 'score' ? 'asc' : 'asc' }
}

function tone(score: number | null): string {
  if (score === null) return ''
  if (score >= 90) return 'good'
  if (score >= 70) return 'warn'
  return 'bad'
}

// ----- Trend (G6 line) -----
const trendEl = ref<HTMLDivElement | null>(null)
let trendGraph: Graph | null = null

// ----- Cross-component graph -----
const refsEl = ref<HTMLDivElement | null>(null)
let refsGraph: Graph | null = null

// ----- Vocabulary noun-verb map -----
const vocabEl = ref<HTMLDivElement | null>(null)
let vocabGraph: Graph | null = null
const vocabDetail = ref<null | { kind: string; label: string; scope?: string; output?: string; judgment?: boolean; deprecated?: string[]; definition?: string; needed?: string }>(null)

onMounted(() => {
  const trend = (d.value.history || []).filter((s) => typeof s.average_score === 'number')
  if (trendEl.value && trend.length >= 2) trendGraph = mountTrend(trendEl.value, trend)
  const refs = d.value.cross_component
  if (refsEl.value && (refs?.nodes?.length ?? 0) > 0) refsGraph = mountRefs(refsEl.value, refs!)
  const vocab = d.value.vocabulary
  if (vocabEl.value && vocab && (vocab.verbs?.length ?? 0) > 0) vocabGraph = mountVocab(vocabEl.value, vocab)
})
onBeforeUnmount(() => {
  trendGraph?.destroy()
  refsGraph?.destroy()
  vocabGraph?.destroy()
})

function mountTrend(container: HTMLDivElement, history: HistoryPoint[]): Graph {
  const sorted = [...history].sort((a, b) => (a.timestamp || '').localeCompare(b.timestamp || ''))
  const W = 700, H = 200
  const nodes = sorted.map((s, i) => ({
    id: `t${i}`,
    data: { label: `${Math.round(s.average_score)}`, ts: s.timestamp || '' },
    style: {
      x: 60 + i * Math.max(40, (W - 120) / Math.max(1, sorted.length - 1)),
      y: H - 20 - (s.average_score / 100) * (H - 60),
      size: 8,
      fill: '#2b5fff',
      labelText: `${Math.round(s.average_score)}`,
      labelFontSize: 11,
      labelPosition: 'top',
      labelOffsetY: -4,
    },
  }))
  const edges = sorted.slice(1).map((_, i) => ({
    source: `t${i}`,
    target: `t${i + 1}`,
    style: { stroke: '#88a', lineWidth: 2 },
  }))
  const g = new Graph({
    container,
    data: { nodes, edges },
    node: { type: 'circle' },
    edge: { type: 'line' },
    behaviors: ['zoom-canvas', 'drag-canvas'],
    autoFit: 'view',
  })
  g.render()
  return g
}

function mountVocab(container: HTMLDivElement, vocab: any): Graph {
  // Compound containers per scope.
  //   Verbs            → rounded rectangles, label CENTERED inside the rect
  //   Nouns            → circles, label to the RIGHT of the circle
  //   Deferred verbs   → dashed rectangles, faded text
  //   Cross-scope verbs (scan/test/discover) → 3px outline
  // Click any node → side-panel detail.
  const homonyms: string[] = vocab.cross_scope_homonyms || []
  const combos = (vocab.scopes || []).map((s: any) => ({
    id: `combo-${s.id}`,
    data: { label: s.label || s.id },
    style: {
      fill: s.id === 'auditor' ? 'rgba(139,63,255,0.05)' : 'rgba(43,95,255,0.05)',
      stroke: s.id === 'auditor' ? '#8b3fff' : '#2b5fff',
      lineDash: [6, 4],
      lineWidth: 1.5,
      radius: 12,
      labelText: s.label || s.id,
      labelFontSize: 13,
      labelFontWeight: 600,
      labelFill: s.id === 'auditor' ? '#8b3fff' : '#2b5fff',
      labelPosition: 'top',
      labelOffsetY: -10,
    },
  }))

  const nodes: any[] = []

  // --- VERBS — rounded rectangles, label inside ---
  for (const v of vocab.verbs || []) {
    const isHomonym = homonyms.includes(v.id)
    nodes.push({
      id: `verb-${v.id}`,
      combo: `combo-${v.scope}`,
      data: { kind: 'verb', label: v.id, scope: v.scope, output: v.output, judgment: v.judgment, deprecated: v.deprecated || [] },
      style: {
        // Node shape is set globally via the `node.type` function below.
        size: [Math.max(56, v.id.length * 9 + 18), 30],
        fill: v.judgment
          ? (v.scope === 'auditor' ? '#dabffa' : '#fbe6a8')
          : (v.scope === 'auditor' ? '#e7d6fa' : '#dbe5fc'),
        stroke: v.scope === 'auditor' ? '#8b3fff' : '#2b5fff',
        lineWidth: isHomonym ? 3 : 1.6,
        radius: 14,
        shadowColor: 'rgba(15,20,40,0.08)',
        shadowBlur: 4,
        shadowOffsetY: 1,
        // Label placement: center of the rect, both axes.
        labelText: v.id,
        labelFontSize: 12,
        labelFontWeight: 600,
        labelFill: '#1d2433',
        labelPlacement: 'center',
        labelPosition: 'center',
        labelTextAlign: 'center',
        labelTextBaseline: 'middle',
      },
    })
  }

  // --- NOUNS — ellipses, label CENTERED inside ---
  // Ellipses (instead of circles) so labels like "frontmatter" actually
  // fit inside the shape. Width grows with label length.
  for (const n of vocab.nouns || []) {
    const w = Math.max(60, n.id.length * 8 + 18)
    const h = n.class === 'role_nouns' ? 24 : 28
    nodes.push({
      id: `noun-${n.id}`,
      combo: n.scope ? `combo-${n.scope}` : undefined,
      data: { kind: 'noun', label: n.id, class: n.class, definition: n.definition },
      style: {
        size: [w, h],
        fill: n.class === 'output_class' ? '#ffd58a' : n.class === 'role_nouns' ? '#ffe9c7' : '#ffc46e',
        stroke: '#e07a13',
        lineWidth: 1.5,
        shadowColor: 'rgba(15,20,40,0.08)',
        shadowBlur: 4,
        shadowOffsetY: 1,
        labelText: n.id,
        labelFontSize: n.class === 'role_nouns' ? 10 : 11,
        labelFontWeight: 500,
        labelFill: '#1d2433',
        labelPlacement: 'center',
        labelPosition: 'center',
        labelTextAlign: 'center',
        labelTextBaseline: 'middle',
      },
    })
  }

  // --- DEFERRED — dashed rectangles, faded text ---
  for (const def of vocab.deferred || []) {
    nodes.push({
      id: `def-${def.verb}`,
      combo: def.scope ? `combo-${def.scope}` : undefined,
      data: { kind: 'deferred', label: def.verb, scope: def.scope, needed: def.needed_warrant },
      style: {
        size: [Math.max(56, def.verb.length * 9 + 18), 30],
        fill: '#fafbff',
        stroke: '#888',
        lineDash: [6, 4],
        lineWidth: 1.5,
        radius: 14,
        labelText: def.verb,
        labelFontSize: 12,
        labelFontWeight: 500,
        labelFill: '#666',
        labelPlacement: 'center',
        labelPosition: 'center',
        labelTextAlign: 'center',
        labelTextBaseline: 'middle',
      },
    })
  }

  // --- EDGES — curved, color by relationship type ---
  const edges = (vocab.edges || []).map((e: any) => ({
    source: `verb-${e.source}`,
    target: `noun-${e.target}`,
    data: { type: e.type },
    style: {
      stroke: e.type === 'acts_as' ? '#bbb' : '#5a87ff',
      lineDash: e.type === 'acts_as' ? [4, 3] : undefined,
      lineWidth: 1.4,
      endArrow: true,
      endArrowSize: 7,
      endArrowFill: e.type === 'acts_as' ? '#bbb' : '#5a87ff',
      // Slight curvature for visual breathing room.
      curveness: 0.2,
      opacity: 0.85,
    },
  }))

  const g = new Graph({
    container,
    data: { nodes, edges, combos },
    // Pick the shape per node based on its data.kind. Verbs (and
    // deferred verbs) are rect; nouns are ellipse (so the width/height
    // array applies and the label fits inside the shape).
    node: {
      type: (datum: any) => (datum.data?.kind === 'noun' ? 'ellipse' : 'rect'),
      state: {
        hover: { lineWidth: 3, shadowBlur: 10, shadowColor: 'rgba(43,95,255,0.35)' },
      },
    },
    edge: {
      type: 'cubic-horizontal',
      state: { hover: { stroke: '#1d2433', opacity: 1, lineWidth: 2 } },
    },
    combo: { type: 'rect', padding: 24 },
    layout: {
      type: 'combo-combined',
      outerLayout: { type: 'force', linkDistance: 120, nodeStrength: -260, collideStrength: 0.9 },
      innerLayout: { type: 'grid', cols: 4 },
    },
    behaviors: ['zoom-canvas', 'drag-canvas', 'drag-element',
                { type: 'hover-activate', state: 'hover' }],
    autoFit: 'view',
    padding: 20,
  })

  g.on('node:click', (evt: any) => {
    const datum = g.getNodeData(evt.target.id)
    if (!datum?.data) return
    vocabDetail.value = { ...(datum.data as any) }
  })

  g.render()
  return g
}

function mountRefs(container: HTMLDivElement, refs: { nodes: any[]; edges: any[] }): Graph {
  const g = new Graph({
    container,
    data: {
      nodes: refs.nodes.map((n: any) => ({
        id: n.id,
        data: { label: n.label || n.id, type: n.type || 'artifact' },
        style: {
          size: n.type === 'manifest' ? 24 : 18,
          fill: n.broken ? '#c63030' : '#2b5fff',
          labelText: n.label || n.id,
          labelFontSize: 10,
          labelPosition: 'bottom',
        },
      })),
      edges: (refs.edges || []).map((e: any) => ({
        source: e.source,
        target: e.target,
        style: { stroke: e.broken ? '#c63030' : '#aab', lineDash: e.broken ? [4, 3] : null, endArrow: true },
      })),
    },
    node: { type: 'circle' },
    edge: { type: 'line' },
    layout: { type: 'd3-force', linkDistance: 80, nodeStrength: -120 },
    behaviors: ['zoom-canvas', 'drag-canvas', 'drag-element'],
    autoFit: 'view',
  })
  g.render()
  return g
}
</script>

<template>
  <div class="repo-report">
    <!-- Header -->
    <header class="rr-hdr">
      <div class="rr-hdr-left">
        <h2 class="rr-title">{{ d.project }}</h2>
        <p class="rr-meta">
          <span class="muted">Generated {{ d.generated_at || '—' }}</span>
        </p>
      </div>
      <div class="rr-hdr-right">
        <div class="rr-score" :class="scoreTone">
          <span class="v">{{ d.summary?.average_score ?? '—' }}</span>
          <span class="u">/ 100</span>
        </div>
        <div class="rr-badges">
          <span v-if="d.repo_meta?.security" class="badge" :class="`sec-${d.repo_meta.security}`">{{ d.repo_meta.security }}</span>
          <span v-if="d.repo_meta?.status" class="badge">{{ d.repo_meta.status }}</span>
          <span v-if="d.repo_meta?.stars != null" class="badge">★ {{ d.repo_meta.stars }}</span>
          <span v-if="d.r51_enabled" class="badge"><a href="/reference/rules#R51" class="no-underline">R51 on</a></span>
        </div>
      </div>
    </header>

    <!-- Clean state — when there are no findings -->
    <section v-if="isClean" class="panel clean">
      <h3>Audit clean ·  zero findings</h3>
      <p>
        Every artifact in this repo passes <a href="/reference/rules">all NLPM rules</a> at the time of this audit.
        The methodology — same scorer, checker, and security pipeline used on every external repo — is described
        in <a v-if="d.repo_meta?.audit_report_path" :href="`https://github.com/xiaolai/nlpm-for-claude/blob/main/${d.repo_meta.audit_report_path}`">the audit markdown</a>.
      </p>
    </section>

    <!-- Per-file table — only if files have scores -->
    <section v-if="(d.files || []).length > 0" id="files" class="panel">
      <h3>Per-file scores</h3>
      <p class="hint">{{ d.files.length }} files. Click a column to sort.</p>
      <div class="table-wrap">
        <table class="rr-table">
          <thead>
            <tr>
              <th @click="sortFilesBy('path')" :class="{ active: fileSortKey === 'path' }">Path</th>
              <th @click="sortFilesBy('type')" :class="{ active: fileSortKey === 'type' }">Type</th>
              <th @click="sortFilesBy('score')" :class="{ active: fileSortKey === 'score' }">Score</th>
              <th @click="sortFilesBy('findings')" :class="{ active: fileSortKey === 'findings' }">Findings</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="f in sortedFiles" :key="f.path">
              <td><code>{{ f.path }}</code></td>
              <td>{{ f.type }}</td>
              <td class="r score-cell" :class="tone(f.score)">{{ f.score ?? '—' }}</td>
              <td class="r">{{ f.findings.length }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Trend -->
    <section v-if="(d.history || []).length >= 2" id="trend" class="panel">
      <h3>Score trend</h3>
      <p class="hint">Average score per audit, oldest → newest.</p>
      <div ref="trendEl" class="g6-frame"></div>
    </section>

    <!-- Cross-component graph -->
    <section v-if="(d.cross_component?.nodes?.length ?? 0) > 0" id="refs" class="panel">
      <h3>Cross-component references</h3>
      <p class="hint">Artifacts and their references; broken edges in red.</p>
      <div ref="refsEl" class="g6-frame"></div>
    </section>

    <!-- Vocabulary noun-verb map -->
    <section v-if="(d.vocabulary?.verbs?.length ?? 0) > 0" id="vocab" class="panel">
      <h3>Vocabulary noun-verb map</h3>
      <p class="hint">
        Verbs (rounded rectangles), nouns (circles). Two scopes shown as compound containers.
        <strong>Doubled outlines</strong> = cross-scope homonyms (e.g. <code>scan</code>, <code>test</code>).
        <strong>Dashed boxes</strong> = deferred-pending-warrant (terms with P2–P5 satisfied awaiting P6 evidence; see
        <a href="/reference/principles">principles</a>).
        Click any node for details. Solid arrows = produces; dashed = role-noun pairing.
      </p>
      <div ref="vocabEl" class="g6-frame vocab-frame"></div>
      <aside v-if="vocabDetail" class="vocab-detail">
        <button class="close" @click="vocabDetail = null" aria-label="close">×</button>
        <h4>{{ vocabDetail.label }}</h4>
        <dl>
          <dt>Kind</dt>
          <dd>{{ vocabDetail.kind }}</dd>
          <template v-if="vocabDetail.scope"><dt>Scope</dt><dd>{{ vocabDetail.scope }}</dd></template>
          <template v-if="vocabDetail.output"><dt>Output</dt><dd>{{ vocabDetail.output }}</dd></template>
          <template v-if="vocabDetail.judgment !== undefined"><dt>Judgment?</dt><dd>{{ vocabDetail.judgment ? 'yes' : 'no' }}</dd></template>
          <template v-if="vocabDetail.definition"><dt>Definition</dt><dd>{{ vocabDetail.definition }}</dd></template>
          <template v-if="vocabDetail.deprecated?.length"><dt>Deprecated synonyms</dt><dd>{{ vocabDetail.deprecated.join(', ') }}</dd></template>
          <template v-if="vocabDetail.needed"><dt>Needed warrant</dt><dd>{{ vocabDetail.needed }}</dd></template>
        </dl>
        <p class="learn"><a :href="vocabDetail.kind === 'verb' ? '/reference/vocabulary#vocab-verbs' : vocabDetail.kind === 'deferred' ? '/reference/principles#precedence' : '/reference/vocabulary#vocab-nouns'">Learn more in the framework reference →</a></p>
      </aside>
    </section>

    <!-- Drift candidates -->
    <section v-if="(d.vocab_drift?.candidates?.length ?? 0) > 0" id="drift" class="panel">
      <h3>Vocabulary drift candidates</h3>
      <p class="hint">Registry-free advisory from <code>vocab-drift-scanner</code>.</p>
      <div v-for="(c, i) in d.vocab_drift!.candidates" :key="i" class="drift-card" :class="`conf-${c.confidence}`">
        <div class="terms">{{ c.terms.map((t: string) => `\`${t}\``).join(' ↔ ') }}</div>
        <div class="meta">
          <a href="/reference/drift#disposition-criteria">{{ c.disposition }}</a> ·
          <a href="/reference/drift#confidence-criteria">confidence: {{ c.confidence }}</a> ·
          suggested canonical: <code>{{ c.suggested_canonical }}</code> ·
          {{ c.files_affected }} file(s)
        </div>
        <div v-if="c.evidence" class="meta">{{ c.evidence }}</div>
      </div>
    </section>

    <!-- Findings list -->
    <section v-if="!isClean" id="findings" class="panel">
      <h3>Findings</h3>
      <p class="hint">{{ d.findings.length }} total · grouped by rule. Click a rule_id for its definition.</p>
      <div v-for="g in findingsByRule" :key="g.rule" class="finding-group">
        <h4>
          <a :href="/^R\d+$/.test(g.rule) ? `/reference/rules#${g.rule}` : '/reference/rules'">{{ g.rule }}</a>
          <span class="muted">({{ g.items.length }})</span>
        </h4>
        <div v-for="(f, i) in g.items" :key="i" class="finding-row">
          <a :href="`/reference/scoring#severity-levels`" :class="`sev-${f.severity}`">{{ (f.severity || 'low').toUpperCase() }}</a>
          <code>{{ f.file }}<span v-if="f.line">:{{ f.line }}</span></code>
          <span>{{ f.message }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.repo-report { display: flex; flex-direction: column; gap: 20px; }
.rr-hdr { display: flex; justify-content: space-between; align-items: flex-end; padding: 16px; border: 1px solid var(--vp-c-divider); border-radius: 8px; background: var(--vp-c-bg-soft); }
.rr-title { margin: 0 0 4px; font-size: 18px; font-weight: 600; }
.rr-meta { margin: 0; font-size: 12px; }
.muted { color: var(--vp-c-text-2); }
.rr-score { text-align: right; }
.rr-score .v { font-size: 36px; font-weight: 700; }
.rr-score .u { font-size: 14px; color: var(--vp-c-text-2); margin-left: 2px; }
.rr-score.pass .v { color: #2a8a3d; }
.rr-score.fail .v { color: #c63030; }
.rr-badges { margin-top: 4px; display: flex; gap: 6px; justify-content: flex-end; flex-wrap: wrap; }
.badge { font-size: 11px; padding: 2px 8px; border: 1px solid var(--vp-c-divider); border-radius: 99px; color: var(--vp-c-text-2); }
.badge.sec-CLEAR { color: #2a8a3d; border-color: #2a8a3d; }
.badge.sec-REVIEW { color: #c47c00; border-color: #c47c00; }
.badge.sec-BLOCKED { color: #c63030; border-color: #c63030; }
.badge a, .no-underline { color: inherit; text-decoration: none; }
.panel { padding: 16px; border: 1px solid var(--vp-c-divider); border-radius: 8px; background: var(--vp-c-bg-soft); }
.panel h3 { margin: 0 0 4px; font-size: 15px; font-weight: 600; }
.panel.clean { border-color: #2a8a3d; }
.panel.clean h3 { color: #2a8a3d; }
.hint { margin: 0 0 12px; font-size: 12px; color: var(--vp-c-text-2); }
.table-wrap { overflow-x: auto; }
.rr-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.rr-table th, .rr-table td { padding: 5px 8px; border-bottom: 1px solid var(--vp-c-divider); text-align: left; }
.rr-table th { background: var(--vp-c-bg); cursor: pointer; user-select: none; font-weight: 600; }
.rr-table th.active { color: var(--vp-c-brand-1); }
.rr-table td.r, .rr-table th:nth-child(3), .rr-table th:nth-child(4) { text-align: right; }
.score-cell.good { color: #2a8a3d; font-weight: 600; }
.score-cell.warn { color: #c47c00; font-weight: 600; }
.score-cell.bad { color: #c63030; font-weight: 600; }
.g6-frame { width: 100%; height: 320px; border: 1px solid var(--vp-c-divider); border-radius: 6px; background: var(--vp-c-bg); position: relative; }
.vocab-frame { height: 580px; }
.vocab-detail { margin-top: 12px; padding: 12px 14px; background: var(--vp-c-bg); border: 1px solid var(--vp-c-divider); border-radius: 6px; position: relative; max-width: 520px; }
.vocab-detail h4 { margin: 0 0 8px; font-size: 14px; }
.vocab-detail dl { margin: 0; display: grid; grid-template-columns: 110px 1fr; column-gap: 12px; row-gap: 4px; font-size: 12px; }
.vocab-detail dt { color: var(--vp-c-text-2); }
.vocab-detail dd { margin: 0; }
.vocab-detail .learn { font-size: 12px; margin: 10px 0 0; }
.vocab-detail .close { position: absolute; top: 6px; right: 8px; background: none; border: none; font-size: 18px; cursor: pointer; color: var(--vp-c-text-2); }
.drift-card { padding: 10px 12px; border-left: 4px solid var(--vp-c-divider); background: var(--vp-c-bg); border-radius: 4px; margin-bottom: 8px; }
.drift-card.conf-high { border-left-color: #c63030; }
.drift-card.conf-medium { border-left-color: #c47c00; }
.drift-card.conf-low { border-left-color: var(--vp-c-text-2); }
.drift-card .terms { font-weight: 600; }
.drift-card .meta { font-size: 12px; color: var(--vp-c-text-2); margin-top: 4px; }
.finding-group { margin-bottom: 16px; }
.finding-group h4 { margin: 0 0 6px; font-size: 13px; color: var(--vp-c-brand-1); }
.finding-row { display: grid; grid-template-columns: 70px minmax(160px, 1.6fr) 2.4fr; gap: 10px; padding: 6px 0; font-size: 13px; border-bottom: 1px dashed var(--vp-c-divider); align-items: start; }
.finding-row > * { min-width: 0; overflow-wrap: break-word; }
.finding-row code { word-break: break-all; }
.sev-high { color: #c63030; font-weight: 600; text-decoration: none; border-bottom: 1px dotted currentColor; }
.sev-medium { color: #c47c00; font-weight: 600; text-decoration: none; border-bottom: 1px dotted currentColor; }
.sev-low { color: var(--vp-c-text-2); text-decoration: none; border-bottom: 1px dotted currentColor; }
</style>
