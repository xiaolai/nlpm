// nlpm-dashboard.js — auditor aggregate dashboard panels.

(function () {
  "use strict";
  const dataEl = document.getElementById("nlpm-data");
  if (!dataEl) return;
  const D = JSON.parse(dataEl.textContent || "{}");

  // ------------------------------------------------------------------
  // KPI tiles in the header
  // ------------------------------------------------------------------
  const kpiGrid = document.getElementById("kpi-grid");
  const s = D.summary || {};
  const tiles = [
    { v: s.total_repos ?? 0, l: "repos" },
    { v: s.total_findings ?? 0, l: "findings" },
    { v: s.total_advisories ?? 0, l: "advisories" },
    { v: s.repos_with_drift ?? 0, l: "with drift" },
  ];
  kpiGrid.innerHTML = tiles.map(t => `
    <div class="kpi"><div class="v">${t.v}</div><div class="l">${t.l}</div></div>
  `).join("");

  // ------------------------------------------------------------------
  // Repos table — sortable
  // ------------------------------------------------------------------
  const rows = (D.repo_rows || []).slice();
  let sortKey = "total_findings";
  let sortDir = "desc";

  const cmp = (a, b) => {
    const av = a[sortKey];
    const bv = b[sortKey];
    if (typeof av === "number" && typeof bv === "number") {
      return sortDir === "asc" ? av - bv : bv - av;
    }
    const sa = String(av ?? "");
    const sb = String(bv ?? "");
    return sortDir === "asc" ? sa.localeCompare(sb) : sb.localeCompare(sa);
  };

  const slugFor = (repo) => repo.replace(/\//g, "-");

  const renderRepoTable = () => {
    rows.sort(cmp);
    const body = document.querySelector("#repo-table tbody");
    body.innerHTML = rows.map(r => {
      const slug = slugFor(r.repo);
      const repoCell = `<a href="./${escapeHtml(slug)}.html" title="Open per-repo report"><code>${escapeHtml(r.repo)}</code></a>`;
      return `
      <tr>
        <td>${repoCell}</td>
        <td>${escapeHtml(r.status || "—")}</td>
        <td>${r.stars ?? "—"}</td>
        <td>${r.score ?? "—"}</td>
        <td class="security-cell sec-${escapeHtml(r.security || "UNKNOWN")}">${escapeHtml(r.security || "—")}</td>
        <td>${r.total_findings || 0}</td>
        <td>${r.high_findings || 0}</td>
        <td>${r.vocab_drift_count || 0}${r.vocab_drift_high ? ` <span class="muted">(${r.vocab_drift_high} high)</span>` : ""}</td>
      </tr>
      `;
    }).join("");
    document.querySelectorAll("#repo-table th").forEach((th) => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.sort === sortKey) th.classList.add(sortDir === "asc" ? "sort-asc" : "sort-desc");
    });
  };

  document.querySelectorAll("#repo-table th").forEach((th) => {
    th.addEventListener("click", () => {
      const k = th.dataset.sort;
      if (sortKey === k) sortDir = sortDir === "asc" ? "desc" : "asc";
      else { sortKey = k; sortDir = "desc"; }
      renderRepoTable();
    });
  });
  renderRepoTable();

  // ------------------------------------------------------------------
  // Rule distribution — bar via G6 + plain table
  // ------------------------------------------------------------------
  const rules = D.rule_distribution || [];
  if (rules.length > 0) {
    renderRuleBars(rules);
    const ruleHref = (rid) => /^R\d+$/.test(rid) ? `./docs/index.html#${rid}` : "./docs/index.html#rules";
    document.getElementById("rule-table-wrap").innerHTML = `
      <table>
        <thead><tr><th>Rule</th><th class="r">Occurrences</th><th class="r">Repos affected</th></tr></thead>
        <tbody>${rules.map(r => `
          <tr>
            <td><a href="${ruleHref(r.rule_id)}" class="doc-link"><code>${escapeHtml(r.rule_id)}</code></a></td>
            <td class="r">${r.total}</td>
            <td class="r">${r.repos_affected}</td>
          </tr>
        `).join("")}</tbody>
      </table>
    `;
  } else {
    document.getElementById("rule-graph").innerHTML =
      `<div style="padding:24px;color:var(--fg-muted);">No findings logged yet.</div>`;
  }

  // ------------------------------------------------------------------
  // Cross-repo drift network — G6 force
  // ------------------------------------------------------------------
  const net = D.drift_network || { nodes: [], edges: [] };
  if ((net.nodes || []).length > 0) {
    renderDriftNetwork(net);
  } else {
    document.getElementById("drift-graph").innerHTML =
      `<div style="padding:24px;color:var(--fg-muted);">No vocab-drift advisories logged yet. The cross-repo drift network appears once <code>auditor-vocab-drift</code> has produced records.</div>`;
  }

  // ------------------------------------------------------------------
  // Activity timeline — G6 polyline per event type
  // ------------------------------------------------------------------
  const tl = D.activity_timeline || [];
  if (tl.length >= 2) {
    renderActivityTimeline(tl);
  } else {
    document.getElementById("activity-graph").innerHTML =
      `<div style="padding:24px;color:var(--fg-muted);">Need at least 2 days of events to render a timeline.</div>`;
  }

  // ==================================================================
  // G6 renderers
  // ==================================================================

  function renderRuleBars(items) {
    // Render the chart on a transparent canvas. Bars come from G6; the
    // rotated rule-id labels are HTML elements absolutely positioned
    // over the canvas — far easier than fighting G6's label rotation,
    // gives us clean kerning + theme-adaptive text color via inherited CSS.
    const container = document.getElementById("rule-graph");
    container.style.position = "relative";
    container.innerHTML = ""; // wipe any prior render
    const N = items.length;
    const W = 800;
    const H = 280; // taller so rotated labels have room below the axis
    const margin = 40;
    const labelGutter = 90; // vertical room reserved for rotated labels
    const baselineY = H - labelGutter;
    const maxVal = Math.max(...items.map(i => i.total));
    const slot = (W - 2 * margin) / Math.max(1, N);

    const nodes = [];
    items.forEach((it, i) => {
      const h = (it.total / maxVal) * (baselineY - 20);
      const cx = margin + i * slot + slot / 2;
      nodes.push({
        id: `r${i}`,
        data: { label: it.rule_id, val: it.total, repos: it.repos_affected },
        style: {
          x: cx,
          y: baselineY - h / 2,
          size: [Math.max(8, slot * 0.7), Math.max(2, h)],
          fill: "#2b5fff",
        },
      });
    });

    const graph = new G6.Graph({
      container: "rule-graph",
      data: { nodes, edges: [] },
      node: { type: "rect" },
      behaviors: ["zoom-canvas", "drag-canvas"],
      autoFit: "view",
    });
    graph.render();

    // Overlay rotated labels in a separate absolutely-positioned layer.
    // Coordinates are computed using G6's input coords; we then scale to
    // the rendered container size since autoFit may have resized the SVG.
    const overlay = document.createElement("div");
    overlay.className = "rule-label-overlay";
    Object.assign(overlay.style, {
      position: "absolute",
      inset: "0",
      pointerEvents: "none",
      // Match G6's internal coordinate system; the chart is rendered
      // with viewBox-ish autoFit, so we use percentages.
    });
    // To map coords correctly under autoFit, compute the visible scale.
    requestAnimationFrame(() => {
      const cw = container.clientWidth;
      const ch = container.clientHeight;
      // G6's autoFit fits content into the container; preserve aspect.
      const sx = cw / W;
      const sy = ch / H;
      const s = Math.min(sx, sy);
      const offX = (cw - W * s) / 2;
      const offY = (ch - H * s) / 2;

      items.forEach((it, i) => {
        const cx = (margin + i * slot + slot / 2) * s + offX;
        const top = baselineY * s + offY + 4;
        const label = document.createElement("div");
        label.textContent = it.rule_id;
        Object.assign(label.style, {
          position: "absolute",
          left: cx + "px",
          top: top + "px",
          fontSize: "10px",
          fontFamily: "inherit",
          color: "var(--vp-c-text-2, #5a6378)",
          whiteSpace: "nowrap",
          transformOrigin: "left top",
          transform: "rotate(35deg)",
        });
        overlay.appendChild(label);
      });
      container.appendChild(overlay);
    });
  }

  function renderDriftNetwork(net) {
    const maxFreq = Math.max(1, ...net.nodes.map(n => n.freq || 1));
    const nodes = net.nodes.map(n => ({
      id: n.id,
      data: { label: n.label, freq: n.freq, repos: n.repos },
      style: {
        size: 14 + 30 * Math.sqrt((n.freq || 1) / maxFreq),
        fill: n.freq >= 3 ? "#c63030" : n.freq >= 2 ? "#c47c00" : "#2b5fff",
        labelText: n.label,
        labelFontSize: 11,
        labelPosition: "bottom",
      },
    }));
    const maxWeight = Math.max(1, ...net.edges.map(e => e.weight || 1));
    const edges = net.edges.map(e => ({
      source: e.source,
      target: e.target,
      data: { weight: e.weight, repos: e.repos },
      style: {
        stroke: "#8888aa",
        lineWidth: 1 + 4 * ((e.weight || 1) / maxWeight),
        opacity: 0.4 + 0.6 * ((e.weight || 1) / maxWeight),
      },
    }));
    const graph = new G6.Graph({
      container: "drift-graph",
      data: { nodes, edges },
      node: { type: "circle" },
      edge: { type: "line" },
      layout: { type: "d3-force", linkDistance: 70, nodeStrength: -180 },
      behaviors: ["zoom-canvas", "drag-canvas", "drag-element"],
      autoFit: "view",
    });
    graph.on("node:click", (evt) => {
      const datum = graph.getNodeData(evt.target.id);
      if (!datum) return;
      const d = datum.data || {};
      alert(
        `Term: ${d.label}\n` +
        `Appears in ${d.freq || 0} clusters across ${(d.repos || []).length} repos:\n` +
        (d.repos || []).map(r => `  - ${r}`).join("\n")
      );
    });
    graph.render();
  }

  function renderActivityTimeline(tl) {
    // Pick top 5 event types by total volume
    const totals = {};
    for (const day of tl) {
      for (const [k, v] of Object.entries(day.counts || {})) {
        totals[k] = (totals[k] || 0) + v;
      }
    }
    const topEvents = Object.entries(totals).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k]) => k);
    const palette = ["#2b5fff", "#8b3fff", "#ff9d2b", "#2a8a3d", "#c63030"];

    const W = 900, H = 240, margin = 40;
    const days = tl.map(d => d.day);
    const maxVal = Math.max(1, ...tl.flatMap(d => topEvents.map(e => d.counts?.[e] || 0)));
    const xStep = (W - 2 * margin) / Math.max(1, days.length - 1);

    const nodes = [];
    const edges = [];
    topEvents.forEach((ev, evIdx) => {
      tl.forEach((day, i) => {
        const id = `${ev}-${i}`;
        const val = day.counts?.[ev] || 0;
        nodes.push({
          id,
          data: { label: `${ev}: ${val}`, day: day.day },
          style: {
            x: margin + i * xStep,
            y: H - margin - (val / maxVal) * (H - 2 * margin),
            size: 4,
            fill: palette[evIdx],
          },
        });
        if (i > 0) {
          edges.push({
            source: `${ev}-${i - 1}`,
            target: id,
            style: { stroke: palette[evIdx], lineWidth: 1.5, opacity: 0.8 },
          });
        }
      });
    });

    const graph = new G6.Graph({
      container: "activity-graph",
      data: { nodes, edges },
      node: { type: "circle" },
      edge: { type: "line" },
      behaviors: ["zoom-canvas", "drag-canvas"],
      autoFit: "view",
    });
    graph.render();

    // Append a legend in the panel
    const legend = topEvents.map((ev, i) => `
      <span style="display:inline-block;margin-right:12px;font-size:12px;">
        <span style="display:inline-block;width:10px;height:10px;background:${palette[i]};border-radius:50%;vertical-align:middle;margin-right:4px;"></span>
        <code>${escapeHtml(ev)}</code> (${totals[ev]})
      </span>
    `).join("");
    const wrap = document.createElement("div");
    wrap.style.marginTop = "8px";
    wrap.innerHTML = legend;
    document.getElementById("activity").appendChild(wrap);
  }

  function escapeHtml(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
})();
