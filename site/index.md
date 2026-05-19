---
layout: home

hero:
  name: NLPM
  text: Natural Language Programming Manager
  tagline: |
    Scores, audits, and disciplines natural-language artifacts in
    Claude Code plugins. 51 rules, 6 vocabulary principles, cross-repo
    dashboards, registry-free drift detection.
  actions:
    - theme: brand
      text: Install
      link: /install
    - theme: alt
      text: Reference
      link: /reference/
    - theme: alt
      text: Auditor dashboard
      link: /dashboard.html
    - theme: alt
      text: GitHub
      link: https://github.com/xiaolai/nlpm-for-claude

features:
  - icon:
      src: /icons/bar-chart-3.svg
      width: 32
      height: 32
    title: 100-point scoring
    details: |
      Deterministic, penalty-based quality scoring for every NL artifact —
      skills, agents, commands, rules, hooks, CLAUDE.md. Anchored in 51
      rules with bright-line definitions and bad/good examples.
  - icon:
      src: /icons/compass.svg
      width: 32
      height: 32
    title: Vocabulary discipline (R51)
    details: |
      Opt-in controlled-vocabulary enforcement. Bootstrap a registry
      from your corpus, declare canonical noun/verb pairs, and let
      `/nlpm:check` flag drift. Registry-free `/nlpm:vocab-drift`
      runs as a no-commitment health check.
  - icon:
      src: /icons/link-2.svg
      width: 32
      height: 32
    title: Cross-component checks
    details: |
      Manifest-vs-disk consistency, broken references, orphan
      components, behavioral contradictions. The single check that
      no other Claude Code validator covers systematically.
  - icon:
      src: /icons/globe.svg
      width: 32
      height: 32
    title: Auditor pipeline
    details: |
      Continuous audits of public Claude Code plugins. Findings,
      vocabulary drift, security signals — all on one cross-repo
      dashboard.
  - icon:
      src: /icons/package.svg
      width: 32
      height: 32
    title: Standalone CLI
    details: |
      `bin/nlpm-check` is a single-file Python (stdlib only). Drop into
      pre-commit hooks or CI without Claude Code installed.
  - icon:
      src: /icons/book-open.svg
      width: 32
      height: 32
    title: Self-evolving rules
    details: |
      Audits feed `rule-health.py`. Rules with high false-positive rate
      surface for refinement; rules with strong real-world warrant become
      exemplars cited in the docs.
---

## What NLPM does, in one paragraph

It treats natural-language artifacts as code. A 100-point rubric, 51 rules anchored in primary sources, cross-component manifest-vs-disk checks, opt-in vocabulary discipline (R51) backed by a six-principle framework derived from OntoClean, DDD, ISO 25964, and BPMN/Event Storming. Everything runs locally as Claude Code slash commands, and there's a continuous auditor pipeline that scores public plugins and feeds findings back into the rulebook.

## Quick links

- **[/install](/install)** — get started in 30 seconds
- **[/reference/](/reference/)** — full framework guide (R01–R51, P1–P6, vocabulary concepts)
- **[/dashboard.html](/dashboard.html)** — cross-repo audit dashboard (200+ plugins)
- **[GitHub](https://github.com/xiaolai/nlpm-for-claude)** — source, issues, releases
