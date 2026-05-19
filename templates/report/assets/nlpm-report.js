// nlpm-report.js — builds all panels from the embedded JSON blob.
// Depends on G6 v5 (window.G6) loaded by ./vendor/g6.min.js.

(function () {
  "use strict";
  const dataEl = document.getElementById("nlpm-data");
  if (!dataEl) return;
  const D = JSON.parse(dataEl.textContent || "{}");

  // ------------------------------------------------------------------
  // Header
  // ------------------------------------------------------------------
  const scoreBig = document.getElementById("score-big");
  const scoreMeta = document.getElementById("score-meta");
  const avg = D.summary?.average_score;
  const threshold = D.score_threshold ?? 70;
  if (avg !== undefined && avg !== null) {
    scoreBig.textContent = Math.round(avg);
    scoreBig.classList.add(avg >= threshold ? "score-pass" : "score-fail");
    // Header text built with anchor links into the framework guide.
    scoreBig.title = "Click for score bands";
    scoreBig.style.cursor = "pointer";
    scoreBig.addEventListener("click", () => location.href = "./docs/index.html#score-bands");
    if (D.repo_meta) {
      const m = D.repo_meta;
      const parts = [];
      if (m.security) parts.push(`security: ${escapeHtml(m.security)}`);
      if (m.status) parts.push(`status: ${escapeHtml(m.status)}`);
      if (m.stars !== null && m.stars !== undefined) parts.push(`★ ${m.stars}`);
      parts.push(`<a href="./docs/index.html#score-bands" class="doc-link">threshold ${threshold}</a>`);
      scoreMeta.innerHTML = parts.join(" · ");
    } else {
      const pass = D.summary?.pass_count ?? 0;
      const total = D.summary?.total_files ?? 0;
      const r51 = D.r51_enabled
        ? `<a href="./docs/index.html#R51" class="doc-link">R51 on</a>`
        : `<a href="./docs/index.html#R51" class="doc-link">R51 off</a>`;
      scoreMeta.innerHTML = `${pass}/${total} pass · <a href="./docs/index.html#score-bands" class="doc-link">threshold ${threshold}</a> · ${r51}`;
    }
  } else {
    scoreBig.textContent = "—";
    scoreMeta.textContent = "no data";
  }

  // ------------------------------------------------------------------
  // Per-file score table with sortable columns
  // ------------------------------------------------------------------
  const tableBody = document.querySelector("#score-table tbody");
  const files = Array.isArray(D.files) ? D.files.slice() : [];
  let sortKey = "score";
  let sortDir = "asc";

  const cmp = (a, b) => {
    const av = a[sortKey], bv = b[sortKey];
    const findA = (a.findings || []).length;
    const findB = (b.findings || []).length;
    if (sortKey === "findings") return sortDir === "asc" ? findA - findB : findB - findA;
    if (typeof av === "number" && typeof bv === "number") {
      return sortDir === "asc" ? av - bv : bv - av;
    }
    const sa = String(av || ""), sb = String(bv || "");
    return sortDir === "asc" ? sa.localeCompare(sb) : sb.localeCompare(sa);
  };

  const renderScoreTable = () => {
    files.sort(cmp);
    tableBody.innerHTML = "";
    for (const f of files) {
      const row = document.createElement("tr");
      const sc = typeof f.score === "number" ? f.score : null;
      const tone = sc === null ? "" : sc >= 90 ? "good" : sc >= 70 ? "warn" : "bad";
      row.innerHTML = `
        <td><code>${escapeHtml(f.path || "")}</code></td>
        <td>${escapeHtml(f.type || "")}</td>
        <td class="score-cell ${tone}">${sc === null ? "—" : sc}</td>
        <td>${(f.findings || []).length}</td>
      `;
      tableBody.appendChild(row);
    }
    // Update header indicators
    document.querySelectorAll("#score-table th").forEach((th) => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.sort === sortKey) th.classList.add(sortDir === "asc" ? "sort-asc" : "sort-desc");
    });
  };

  document.querySelectorAll("#score-table th").forEach((th) => {
    th.addEventListener("click", () => {
      const key = th.dataset.sort;
      if (sortKey === key) sortDir = sortDir === "asc" ? "desc" : "asc";
      else { sortKey = key; sortDir = key === "score" ? "asc" : "asc"; }
      renderScoreTable();
    });
  });
  renderScoreTable();

  // ------------------------------------------------------------------
  // Trend (G6 line)
  // ------------------------------------------------------------------
  const trendData = Array.isArray(D.history) ? D.history.filter(s => typeof s.average_score === "number") : [];
  if (trendData.length >= 2) {
    renderTrendGraph(trendData);
  } else {
    document.getElementById("trend-graph").innerHTML =
      `<div style="padding:24px;color:var(--fg-muted);">Need at least 2 snapshots to render a trend. Run <code>/nlpm:score</code> over time to build history.</div>`;
  }

  // ------------------------------------------------------------------
  // Cross-component reference graph
  // ------------------------------------------------------------------
  const refs = D.cross_component;
  if (refs && Array.isArray(refs.nodes) && refs.nodes.length > 0) {
    renderRefsGraph(refs);
  } else {
    document.getElementById("refs-graph").innerHTML =
      `<div style="padding:24px;color:var(--fg-muted);">No cross-component data — run <code>/nlpm:check</code> first or include its output in the report.</div>`;
  }

  // ------------------------------------------------------------------
  // Vocabulary noun-verb map
  // ------------------------------------------------------------------
  const vocab = D.vocabulary;
  if (vocab && Array.isArray(vocab.verbs) && vocab.verbs.length > 0) {
    renderVocabGraph(vocab);
  } else {
    document.getElementById("vocab-graph").innerHTML =
      `<div style="padding:24px;color:var(--fg-muted);">No vocabulary skill detected (or none parsed). Run <code>/nlpm:vocab-init</code> to bootstrap one.</div>`;
  }

  // ------------------------------------------------------------------
  // Drift candidates
  // ------------------------------------------------------------------
  const driftList = document.getElementById("drift-list");
  const drift = D.vocab_drift?.candidates || [];
  if (drift.length === 0) {
    driftList.innerHTML = `<p class="muted">No drift candidates. Either the corpus is consistent, or <code>/nlpm:vocab-drift</code> hasn't been run.</p>`;
  } else {
    driftList.innerHTML = drift.map((d) => `
      <div class="drift-card conf-${d.confidence || "low"}">
        <div class="terms">${(d.terms || []).map(t => `<code>${escapeHtml(t)}</code>`).join(" ↔ ")}</div>
        <div class="meta">
          <a href="./docs/index.html#disposition-criteria" class="doc-link">${escapeHtml(d.disposition || "")}</a> ·
          <a href="./docs/index.html#confidence-criteria" class="doc-link">confidence: ${escapeHtml(d.confidence || "?")}</a> ·
          suggested canonical: <code>${escapeHtml(d.suggested_canonical || "—")}</code> ·
          ${(d.files_affected ?? 0)} file(s)
        </div>
        ${d.evidence ? `<div class="meta">${escapeHtml(d.evidence)}</div>` : ""}
      </div>
    `).join("");
  }

  // ------------------------------------------------------------------
  // Findings grouped by rule
  // ------------------------------------------------------------------
  const findingsEl = document.getElementById("findings-by-rule");
  const findings = Array.isArray(D.findings) ? D.findings : [];
  if (findings.length === 0) {
    findingsEl.innerHTML = `<p class="muted">No findings.</p>`;
  } else {
    const byRule = {};
    for (const f of findings) {
      const k = f.rule || "UNCLASSIFIED";
      (byRule[k] = byRule[k] || []).push(f);
    }
    const ruleKeys = Object.keys(byRule).sort();
    const ruleHref = (k) => /^R\d+$/.test(k) ? `./docs/index.html#${k}` : "./docs/index.html#rules";
    findingsEl.innerHTML = ruleKeys.map((k) => `
      <div class="finding-group">
        <h3><a href="${ruleHref(k)}" class="doc-link">${escapeHtml(k)}</a> <span class="muted">(${byRule[k].length})</span></h3>
        ${byRule[k].map((f) => `
          <div class="finding-row">
            <a href="./docs/index.html#severity-levels" class="doc-link sev-${escapeHtml(f.severity || "low")}">${escapeHtml((f.severity || "low").toUpperCase())}</a>
            <code>${escapeHtml(f.file || "")}${f.line ? ":" + f.line : ""}</code>
            <span>${escapeHtml(f.message || "")}</span>
          </div>
        `).join("")}
      </div>
    `).join("");
  }

  // ==================================================================
  // G6 renderers
  // ==================================================================

  function renderTrendGraph(history) {
    if (!window.G6) {
      document.getElementById("trend-graph").innerHTML = "G6 missing.";
      return;
    }
    const sorted = history.slice().sort((a, b) => (a.timestamp || "").localeCompare(b.timestamp || ""));
    const nodes = sorted.map((s, i) => ({
      id: `t${i}`,
      data: { label: `${Math.round(s.average_score)}`, ts: s.timestamp || "" },
      style: {
        x: 60 + i * Math.max(40, 800 / Math.max(1, sorted.length - 1)),
        y: 200 - (s.average_score / 100) * 160,
      },
    }));
    const edges = sorted.slice(1).map((_, i) => ({
      source: `t${i}`,
      target: `t${i + 1}`,
    }));

    const graph = new G6.Graph({
      container: "trend-graph",
      data: { nodes, edges },
      node: {
        type: "circle",
        style: { size: 8, fill: "#2b5fff", labelText: (d) => d.data.label, labelFontSize: 11, labelPosition: "top", labelOffsetY: -4 },
      },
      edge: { type: "line", style: { stroke: "#88a", lineWidth: 2 } },
      behaviors: ["zoom-canvas", "drag-canvas"],
      autoFit: "view",
    });
    graph.render();
  }

  function renderRefsGraph(refs) {
    const graph = new G6.Graph({
      container: "refs-graph",
      data: {
        nodes: refs.nodes.map((n) => ({
          id: n.id,
          data: { label: n.label || n.id, type: n.type || "artifact" },
          style: {
            size: n.type === "manifest" ? 24 : 18,
            fill: n.broken ? "#c63030" : "#2b5fff",
            labelText: n.label || n.id,
            labelFontSize: 10,
            labelPosition: "bottom",
          },
        })),
        edges: (refs.edges || []).map((e) => ({
          source: e.source,
          target: e.target,
          style: {
            stroke: e.broken ? "#c63030" : "#aab",
            lineDash: e.broken ? [4, 3] : null,
            endArrow: true,
          },
        })),
      },
      node: { type: "circle" },
      edge: { type: "line" },
      layout: { type: "d3-force", linkDistance: 80, nodeStrength: -120 },
      behaviors: ["zoom-canvas", "drag-canvas", "drag-element"],
      autoFit: "view",
    });
    graph.render();
  }

  function renderVocabGraph(vocab) {
    const showDeprecated = () => document.getElementById("vocab-show-deprecated").checked;
    const showDeferred = () => document.getElementById("vocab-show-deferred").checked;
    const showEdges = () => document.getElementById("vocab-show-edges").checked;

    const buildData = () => {
      const nodes = [];
      const edges = [];
      const combos = (vocab.scopes || []).map((s) => ({
        id: `combo-${s.id}`,
        data: { label: s.label || s.id },
        style: {
          fill: s.id === "auditor" ? "rgba(139,63,255,0.04)" : "rgba(43,95,255,0.04)",
          stroke: s.id === "auditor" ? "#8b3fff" : "#2b5fff",
          lineDash: [4, 3],
          labelText: s.label || s.id,
          labelFontSize: 11,
        },
      }));

      // Verbs
      for (const v of vocab.verbs || []) {
        const isHomonym = (vocab.cross_scope_homonyms || []).includes(v.id);
        nodes.push({
          id: `verb-${v.id}`,
          combo: `combo-${v.scope}`,
          data: { kind: "verb", scope: v.scope, label: v.id, judgment: !!v.judgment, deprecated: v.deprecated || [], output: v.output || "" },
          style: {
            size: 26,
            fill: v.scope === "auditor" ? "#e3d5ff" : "#d5e0ff",
            stroke: v.scope === "auditor" ? "#8b3fff" : "#2b5fff",
            lineWidth: isHomonym ? 3 : 1.5,
            labelText: v.id,
            labelFontSize: 11,
            labelPosition: "center",
            labelFill: "#1d2433",
          },
        });
        if (showDeprecated() && (v.deprecated || []).length > 0) {
          for (const dep of v.deprecated) {
            const depId = `dep-${v.id}-${dep}`;
            nodes.push({
              id: depId,
              combo: `combo-${v.scope}`,
              data: { kind: "deprecated", scope: v.scope, label: dep, canonical: v.id },
              style: {
                size: 14,
                fill: "#fff",
                stroke: "#aaa",
                lineDash: [3, 3],
                labelText: dep,
                labelFontSize: 9,
                labelFill: "#888",
                labelPosition: "bottom",
              },
            });
            edges.push({
              source: depId,
              target: `verb-${v.id}`,
              style: { stroke: "#bbb", lineDash: [2, 2], endArrow: true, endArrowSize: 5 },
            });
          }
        }
      }

      // Nouns (artifact-class + output-class flattened)
      for (const n of vocab.nouns || []) {
        nodes.push({
          id: `noun-${n.id}`,
          // Nouns are typically scope-agnostic; only constrain to a combo
          // when the noun is auditor-only.
          combo: n.scope ? `combo-${n.scope}` : undefined,
          data: { kind: "noun", scope: n.scope || null, label: n.id, class: n.class || "artifact", definition: n.definition || "" },
          style: {
            size: 20,
            fill: "#ffe7c2",
            stroke: "#ff9d2b",
            lineWidth: 1.5,
            labelText: n.id,
            labelFontSize: 10,
            labelPosition: "right",
            labelOffsetX: 6,
            labelFill: "#1d2433",
          },
        });
      }

      // Deferred verbs
      if (showDeferred()) {
        for (const d of vocab.deferred || []) {
          const id = `def-${d.id || d.verb || ""}`;
          nodes.push({
            id,
            combo: d.scope ? `combo-${d.scope}` : undefined,
            data: { kind: "deferred", label: d.verb || d.id, needed: d.needed_warrant || "" },
            style: {
              size: 22,
              fill: "#fff",
              stroke: "#888",
              lineDash: [5, 4],
              labelText: d.verb || d.id,
              labelFontSize: 10,
              labelFill: "#666",
              labelPosition: "center",
            },
          });
        }
      }

      // Produces-edges from verbs to nouns
      if (showEdges()) {
        for (const e of vocab.edges || []) {
          const s = `verb-${e.source}`;
          const t = `noun-${e.target}`;
          if (nodes.find((n) => n.id === s) && nodes.find((n) => n.id === t)) {
            edges.push({
              source: s,
              target: t,
              data: { type: e.type || "produces" },
              style: {
                stroke: e.type === "consumes" ? "#aaa" : "#2b5fff",
                lineDash: e.type === "consumes" ? [3, 3] : null,
                endArrow: true,
                endArrowSize: 6,
                lineWidth: 1.2,
              },
            });
          }
        }
      }

      return { nodes, edges, combos };
    };

    let graph = new G6.Graph({
      container: "vocab-graph",
      data: buildData(),
      node: { type: "circle" },
      edge: { type: "line" },
      combo: { type: "rect", padding: 16 },
      layout: { type: "combo-combined", outerLayout: { type: "force", linkDistance: 100, nodeStrength: -200 }, innerLayout: { type: "grid" } },
      behaviors: ["zoom-canvas", "drag-canvas", "drag-element"],
      autoFit: "view",
    });

    graph.on("node:click", (evt) => {
      const node = evt.target;
      const id = node.id;
      const datum = graph.getNodeData(id);
      showDetail(datum);
    });

    graph.render();

    const rerender = () => {
      graph.setData(buildData());
      graph.render();
    };
    document.getElementById("vocab-show-deprecated").addEventListener("change", rerender);
    document.getElementById("vocab-show-deferred").addEventListener("change", rerender);
    document.getElementById("vocab-show-edges").addEventListener("change", rerender);
  }

  function showDetail(datum) {
    const panel = document.getElementById("vocab-detail");
    const title = document.getElementById("vd-title");
    const body = document.getElementById("vd-body");
    if (!datum || !datum.data) { panel.classList.add("hidden"); return; }
    const d = datum.data;
    title.textContent = d.label;
    const rows = [];
    rows.push(["Kind", d.kind || "?"]);
    if (d.scope) rows.push(["Scope", d.scope]);
    if (d.class) rows.push(["Class", d.class]);
    if (d.judgment !== undefined) rows.push(["Judgment?", d.judgment ? "yes" : "no"]);
    if (d.output) rows.push(["Output", d.output]);
    if (d.canonical) rows.push(["Canonical of", d.canonical]);
    if (d.definition) rows.push(["Definition", d.definition]);
    if (d.deprecated && d.deprecated.length) rows.push(["Deprecated synonyms", d.deprecated.join(", ")]);
    if (d.needed) rows.push(["Needed warrant", d.needed]);
    // Anchor to the right doc section based on the node's kind.
    let docAnchor = "vocab";
    if (d.kind === "verb") docAnchor = "vocab-verbs";
    else if (d.kind === "noun") docAnchor = "vocab-nouns";
    else if (d.kind === "deferred") docAnchor = "vocab-deferred-work-documented-not-yet-executed";
    else if (d.kind === "deprecated") docAnchor = "vocab-verbs";
    rows.push(["Learn more", `<a href="./docs/index.html#${docAnchor}" class="doc-link">framework reference</a>`]);
    body.innerHTML = rows.map(([k, v]) => {
      const isHtml = String(v).includes("<a ");
      return `<dt>${escapeHtml(k)}</dt><dd>${isHtml ? v : escapeHtml(String(v))}</dd>`;
    }).join("");
    panel.classList.remove("hidden");
  }
  document.getElementById("vd-close")?.addEventListener("click", () => {
    document.getElementById("vocab-detail").classList.add("hidden");
  });

  // ------------------------------------------------------------------
  // Utility
  // ------------------------------------------------------------------
  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
})();
