// Custom VitePress theme — extends the default theme and registers
// report-rendering Vue components globally so they can be used inside
// any Markdown page via <DashboardPanels :data="..." />.
import DefaultTheme from 'vitepress/theme'
import Layout from './Layout.vue'
import DashboardPanels from './components/DashboardPanels.vue'
import RepoReport from './components/RepoReport.vue'
import './custom.css'
import type { Theme } from 'vitepress'

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('DashboardPanels', DashboardPanels)
    app.component('RepoReport', RepoReport)
  },
} satisfies Theme
