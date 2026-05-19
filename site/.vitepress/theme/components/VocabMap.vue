<!--
  VocabMap.vue — chart-only noun-verb map. No header, no detail panel,
  no controls. Mounts NLPM's own vocabulary into a G6 graph sized for
  the home hero (or any embedded preview).

  Data source: NLPM's per-repo report JSON, where the build pipeline
  already populates the `vocabulary` field.
-->
<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { Graph } from '@antv/g6'
import nlpm from '../data/reports/xiaolai-nlpm-for-claude.json'

const el = ref<HTMLDivElement | null>(null)
let graph: Graph | null = null

onMounted(() => {
  const vocab = (nlpm as any)?.vocabulary
  if (!el.value || !vocab) return
  graph = mountVocab(el.value, vocab)
})
onBeforeUnmount(() => {
  graph?.destroy()
})

function mountVocab(container: HTMLDivElement, vocab: any): Graph {
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
      labelFontSize: 12,
      labelFontWeight: 600,
      labelFill: s.id === 'auditor' ? '#8b3fff' : '#2b5fff',
      labelPosition: 'top',
      labelOffsetY: -8,
    },
  }))

  const nodes: any[] = []
  for (const v of vocab.verbs || []) {
    const isHomonym = homonyms.includes(v.id)
    nodes.push({
      id: `verb-${v.id}`,
      combo: `combo-${v.scope}`,
      data: { kind: 'verb', label: v.id },
      style: {
        size: [Math.max(48, v.id.length * 8 + 14), 26],
        fill: v.judgment
          ? (v.scope === 'auditor' ? '#dabffa' : '#fbe6a8')
          : (v.scope === 'auditor' ? '#e7d6fa' : '#dbe5fc'),
        stroke: v.scope === 'auditor' ? '#8b3fff' : '#2b5fff',
        lineWidth: isHomonym ? 2.5 : 1.4,
        radius: 12,
        labelText: v.id,
        labelFontSize: 11,
        labelFontWeight: 600,
        labelFill: '#1d2433',
        labelPlacement: 'center',
        labelPosition: 'center',
        labelTextAlign: 'center',
        labelTextBaseline: 'middle',
      },
    })
  }
  for (const n of vocab.nouns || []) {
    const w = Math.max(54, n.id.length * 7 + 14)
    nodes.push({
      id: `noun-${n.id}`,
      combo: n.scope ? `combo-${n.scope}` : undefined,
      data: { kind: 'noun', label: n.id },
      style: {
        size: [w, n.class === 'role_nouns' ? 22 : 24],
        fill: n.class === 'output_class' ? '#ffd58a' : n.class === 'role_nouns' ? '#ffe9c7' : '#ffc46e',
        stroke: '#e07a13',
        lineWidth: 1.3,
        labelText: n.id,
        labelFontSize: n.class === 'role_nouns' ? 9 : 10,
        labelFontWeight: 500,
        labelFill: '#1d2433',
        labelPlacement: 'center',
        labelPosition: 'center',
        labelTextAlign: 'center',
        labelTextBaseline: 'middle',
      },
    })
  }
  for (const def of vocab.deferred || []) {
    nodes.push({
      id: `def-${def.verb}`,
      combo: def.scope ? `combo-${def.scope}` : undefined,
      data: { kind: 'deferred', label: def.verb },
      style: {
        size: [Math.max(48, def.verb.length * 8 + 14), 26],
        fill: '#fafbff',
        stroke: '#888',
        lineDash: [5, 4],
        lineWidth: 1.3,
        radius: 12,
        labelText: def.verb,
        labelFontSize: 10,
        labelFontWeight: 500,
        labelFill: '#666',
        labelPlacement: 'center',
        labelPosition: 'center',
        labelTextAlign: 'center',
        labelTextBaseline: 'middle',
      },
    })
  }
  const edges = (vocab.edges || []).map((e: any) => ({
    source: `verb-${e.source}`,
    target: `noun-${e.target}`,
    style: {
      stroke: e.type === 'acts_as' ? '#bbb' : '#5a87ff',
      lineDash: e.type === 'acts_as' ? [4, 3] : undefined,
      lineWidth: 1.2,
      endArrow: true,
      endArrowSize: 6,
      endArrowFill: e.type === 'acts_as' ? '#bbb' : '#5a87ff',
      curveness: 0.2,
      opacity: 0.8,
    },
  }))

  const g = new Graph({
    container,
    data: { nodes, edges, combos },
    node: { type: (datum: any) => (datum.data?.kind === 'noun' ? 'ellipse' : 'rect') },
    edge: { type: 'cubic-horizontal' },
    combo: { type: 'rect', padding: 22 },
    layout: {
      type: 'combo-combined',
      outerLayout: { type: 'force', linkDistance: 110, nodeStrength: -240, collideStrength: 0.9 },
      innerLayout: { type: 'grid', cols: 3 },
    },
    behaviors: ['zoom-canvas', 'drag-canvas', 'drag-element'],
    autoFit: 'view',
    padding: 16,
  })
  g.render()
  return g
}
</script>

<template>
  <div class="hero-vocab">
    <div ref="el" class="hero-vocab-frame"></div>
    <p class="caption">
      NLPM's own vocabulary as a noun-verb map. Click into
      <a href="/reports/xiaolai-nlpm-for-claude#vocab">the self-audit</a> for the interactive panel.
    </p>
  </div>
</template>

<style scoped>
.hero-vocab {
  width: 100%;
  max-width: 560px;
  margin: 0 auto;
}
.hero-vocab-frame {
  width: 100%;
  height: 360px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg);
  position: relative;
  overflow: hidden;
}
.caption {
  margin-top: 8px;
  font-size: 12px;
  color: var(--vp-c-text-2);
  text-align: center;
}
.caption a { color: var(--vp-c-brand-1); }
/* Tighten on smaller screens — the hero stacks on mobile, so we want
   the chart to stay legible without dominating. */
@media (max-width: 768px) {
  .hero-vocab-frame { height: 280px; }
}
</style>
