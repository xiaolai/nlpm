# nlpm.com (VitePress site)

Reference for the public site, moved out of `AGENTS.md`. The binding build and deploy instructions are in `AGENTS.md` § nlpm.com site.

The public site lives in `site/`. Built with VitePress; deployed to the
`gh-pages` branch which GitHub Pages publishes at <https://nlpm.com>.

- `site/index.md`, `site/install.md` — landing + install pages
- `site/.vitepress/config.ts` — site config (nav, sidebar, theme, search)
- `site/reference/*.md` — auto-generated from canonical SKILL.md sources
  by `bin/nlpm-build-reference-md` (pages: rules.md, principles.md,
  vocabulary.md, scoring.md, artifact-types.md, drift.md)
- `site/build.sh` — full build pipeline: regen reference, sync auditor
  outputs (`auditor/reports/*` → `site/public/`), `pnpm install`,
  `pnpm build`. Output: `site/.vitepress/dist/` (ignored).
- Auditor outputs (dashboard.html, 209 per-repo HTMLs, legacy
  single-page `docs/index.html`, `assets/`, `vendor/g6.min.js`) ride into
  the site as static passthrough from `site/public/`. Cross-references
  from reports continue to hit `/docs/index.html#R06` — the legacy
  single-page guide is kept on the site for backward compatibility.
- `pnpm-lock.yaml` is committed; `node_modules/`, `.vitepress/cache/`,
  `.vitepress/dist/`, `public/` are gitignored.

To rebuild locally:

```bash
bash site/build.sh
```

Deployment is automated by `.github/workflows/deploy-site.yml` — it builds
and publishes to the `gh-pages` branch (served at <https://nlpm.com>) on:
- every push to `main` touching site sources or their generators (`site/**`,
  the `bin/nlpm-build-*` scripts, the canonical
  `skills/nlpm/{rules,vocabulary,scoring,conventions}/SKILL.md`, `commands/**`,
  `agents/**`, `auditor/reports/**`, `auditor/exemplars/**`),
- a daily `0 23 * * *` UTC cron, and
- manual `workflow_dispatch`.

No manual copy-into-`gh-pages` step is needed. To force an off-cycle deploy,
run `gh workflow run deploy-site.yml`.

## Related workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| site-validate | PR touching a site input | Runs `bash site/build.sh` and fails the PR if the VitePress build errors (dead links, broken Mermaid, missing canonical sources). Runs on fork PRs too. |
| site-preview | PR from a same-repo branch touching a site input | Builds with `SITE_BASE=/_pr/<n>/`, pushes to `_pr/<n>/` on `gh-pages`, and posts a sticky PR comment with the preview URL. |
| site-preview-cleanup | PR closed | Removes `_pr/<n>/` from `gh-pages` and updates the sticky comment. |
| nlpm-self-check | Push to `main` (outside `auditor/**`, `case-studies/**`, `nlpm-badge.json`) / PR | Runs `bin/nlpm-check` on this repo and refreshes `nlpm-badge.json`. |
