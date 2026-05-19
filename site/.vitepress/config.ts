import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import footnote from 'markdown-it-footnote'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Walk site/case-studies/ at build time and produce a sidebar that
// lists every article newest first. Filenames are YYYY-MM-DD-<slug>.md;
// the H1 of each article becomes the link label.
function caseStudiesSidebar(): Array<{ text: string; link: string }> {
  const dir = path.resolve(__dirname, '..', 'case-studies')
  if (!fs.existsSync(dir)) return []
  const files = fs.readdirSync(dir)
    .filter((f: string) => f.endsWith('.md') && f !== 'index.md')
    .sort()
    .reverse() // YYYY-MM-DD prefix → reverse-sort gives newest first
  return files.map((f: string) => {
    const stem = f.replace(/\.md$/, '')
    const content = fs.readFileSync(path.join(dir, f), 'utf-8')
    const m = content.match(/^#\s+(.+?)\s*$/m)
    const title = m ? m[1].trim() : stem
    return { text: title, link: `/case-studies/${stem}` }
  })
}

export default withMermaid(defineConfig({
  title: 'NLPM',
  description:
    'Natural Language Programming Manager — scores, audits, and disciplines NL artifacts in Claude Code plugins.',
  cleanUrls: true,
  lastUpdated: true,

  // Dead-link policy: case-study articles include relative links back
  // to source paths (../auditor/, ../analysis/, ../bin/) and inter-
  // article references that may not resolve in the deployed tree. These
  // are historical content; we ship them as-is. Other parts of the site
  // (install, how-it-works, reference/*) still fail on dead links.
  ignoreDeadLinks: [
    /^\.\.\//,                  // any relative path going up out of the tree
    /\/auditor\//,              // back-refs to auditor source paths
    /\/analysis\//,             // back-refs to analysis docs
    /\/bin\//,                  // back-refs to scripts
    /wshobson-agents$/,         // known typo in one article (link missing -learnings suffix)
  ],
  // Where to write the build output and where static passthrough lives.
  outDir: '.vitepress/dist',
  // public/ is the standard VitePress static-passthrough directory; the
  // build pipeline copies auditor/reports/* into site/public/ before
  // running `pnpm build`.

  // Markdown extensions:
  //   - markdown-it-footnote: GFM-ish footnote syntax (`text[^1]`,
  //     `[^1]: definition` block at end of file).
  // Mermaid support is added by the withMermaid wrapper below.
  markdown: {
    config: (md) => {
      md.use(footnote)
    },
  },

  // Mermaid plugin config — uses dynamic import so SSR builds work and the
  // mermaid runtime is only loaded on pages that actually contain diagrams.
  mermaid: {
    // mermaid runtime options; defaults are fine, but pick a theme that
    // adapts to VitePress light/dark mode.
    theme: 'default',
  },
  mermaidPlugin: {
    class: 'mermaid-diagram',
  },

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'NLPM — Natural Language Programming Manager' }],
    ['meta', { property: 'og:url', content: 'https://nlpm.com/' }],
    ['meta', {
      property: 'og:description',
      content:
        'A Claude Code plugin that scores, audits, and disciplines natural-language artifacts. ' +
        'Cross-repo dashboards and per-repo audit reports for 200+ Claude Code plugins.',
    }],
  ],

  themeConfig: {
    siteTitle: 'NLPM',

    nav: [
      { text: 'Home', link: '/' },
      { text: 'Install', link: '/install' },
      { text: 'How it works', link: '/how-it-works' },
      { text: 'Case studies', link: '/case-studies/' },
      {
        text: 'Audit data',
        items: [
          { text: 'Dashboard', link: '/dashboard.html' },
          { text: 'Sample repo report', link: '/SuperClaude-Org-SuperClaude_Framework.html' },
        ],
      },
      { text: 'Reference', link: '/reference/' },
      { text: 'GitHub', link: 'https://github.com/xiaolai/nlpm-for-claude' },
    ],

    sidebar: {
      '/reference/': [
        {
          text: 'Framework reference',
          items: [
            { text: 'Overview', link: '/reference/' },
            { text: 'Rules (R01–R51)', link: '/reference/rules' },
            { text: 'Vocabulary principles', link: '/reference/principles' },
            { text: 'Vocabulary concepts', link: '/reference/vocabulary' },
            { text: 'Scoring & severity', link: '/reference/scoring' },
            { text: 'Artifact types', link: '/reference/artifact-types' },
            { text: 'Drift criteria', link: '/reference/drift' },
          ],
        },
      ],
      '/case-studies/': [
        {
          text: 'Case studies',
          items: [
            { text: 'Overview', link: '/case-studies/' },
            ...caseStudiesSidebar(),
          ],
        },
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/xiaolai/nlpm-for-claude' },
    ],

    search: {
      provider: 'local',
    },

    footer: {
      message: 'MIT-licensed Claude Code plugin.',
      copyright: '© xiaolai · Generated from canonical SKILL.md sources',
    },

    editLink: {
      pattern: 'https://github.com/xiaolai/nlpm-for-claude/edit/main/site/:path',
      text: 'Edit this page on GitHub',
    },

    outline: { level: [2, 3], label: 'On this page' },
  },
}))
