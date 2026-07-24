---
title: Featured audits
outline: [2, 2]
---

# Featured audits

A curated subset of the 270+ external repositories NLPM has audited — picked for **institutional credibility** (OpenAI, Google, CNCF), **scale** (10k+ stars), or **engagement** (merged PRs from the contribute pipeline, often paired with a case-study article). Each entry links to its full per-repo report, every merged PR we filed, and the long-form article when one exists.

For the complete data set, see the [dashboard](/dashboard).

## Contents

1. [openai/codex-plugin-cc](#_1-openai-codex-plugin-cc) — 93/100 · case study
2. [google-gemini/gemini-skills](#_2-google-gemini-gemini-skills) — 98/100 · 2 PRs merged
3. [kubesphere/kubesphere](#_3-kubesphere-kubesphere) — 89/100 · 5 PRs merged · case study
4. [code-yeongyu/oh-my-openagent](#_4-code-yeongyu-oh-my-openagent) — 74/100 · 51.9k⭐ · case study
5. [shanraisshan/claude-code-best-practice](#_5-shanraisshan-claude-code-best-practice) — 88/100 · 46k⭐ · 4 PRs merged
6. [safishamsi/graphify](#_6-safishamsi-graphify) — 37k⭐ · case study
7. [luongnv89/claude-howto](#_7-luongnv89-claude-howto) — case study
8. [K-Dense-AI/scientific-agent-skills](#_8-k-dense-ai-scientific-agent-skills) — domain-specialist plugin
9. [mukul975/Anthropic-Cybersecurity-Skills](#_9-mukul975-anthropic-cybersecurity-skills) — security-domain plugin
10. [gotalab/cc-sdd](#_10-gotalab-cc-sdd) — case study
11. [See also](#see-also)

## 1. openai/codex-plugin-cc

OpenAI's official Codex-for-Claude-Code plugin. Audit score 93/100, security REVIEW. We tracked PR outcomes (no merge state recorded in the events log) and published the [case-study article](/case-studies/2026-04-07-openai-codex-plugin-cc) describing what we found.

- **Per-repo report**: [/reports/openai-codex-plugin-cc](/reports/openai-codex-plugin-cc)
- **Repo**: <https://github.com/openai/codex-plugin-cc>

## 2. google-gemini/gemini-skills

Google's official Gemini skill catalog. Audit score **98/100**, security PASS. Two merged PRs landed naming-convention fixes (the same fixes we discovered with `lijigang/ljg-skills` that were later validated by official Claude Code docs).

- **Per-repo report**: [/reports/google-gemini-gemini-skills](/reports/google-gemini-gemini-skills)
- **Merged PRs**: [#37](https://github.com/google-gemini/gemini-skills/pull/37) · [#38](https://github.com/google-gemini/gemini-skills/pull/38)
- **Repo**: <https://github.com/google-gemini/gemini-skills>

## 3. kubesphere/kubesphere

CNCF cloud-native platform. Audit score 89/100, security REVIEW. Five PRs merged into a major production project — the highest-volume single engagement in the auditor's history. [Case study](/case-studies/2026-05-07-kubesphere-kubesphere) walks through what each PR fixed.

- **Per-repo report**: [/reports/kubesphere-kubesphere](/reports/kubesphere-kubesphere)
- **Merged PRs**: [#6632](https://github.com/kubesphere/kubesphere/pull/6632) · [#6633](https://github.com/kubesphere/kubesphere/pull/6633) · [#6634](https://github.com/kubesphere/kubesphere/pull/6634) · [#6635](https://github.com/kubesphere/kubesphere/pull/6635) · [#6636](https://github.com/kubesphere/kubesphere/pull/6636)
- **Repo**: <https://github.com/kubesphere/kubesphere>

## 4. code-yeongyu/oh-my-openagent

51,912 stars at audit time — the most-starred external repo with a merged engagement. Audit score 74/100 (REVIEW track for security). One PR merged; the [case study](/case-studies/2026-05-07-code-yeongyu-oh-my-openagent) covers the bug-grade vs. quality-grade finding split.

- **Per-repo report**: [/reports/code-yeongyu-oh-my-openagent](/reports/code-yeongyu-oh-my-openagent)
- **Merged PRs**: [#3578](https://github.com/code-yeongyu/oh-my-openagent/pull/3578)
- **Repo**: <https://github.com/code-yeongyu/oh-my-openagent>

## 5. shanraisshan/claude-code-best-practice

46,008 stars. Audit score 88/100, security CLEAR. Four merged PRs touching naming, frontmatter, and example-block discipline. [Case study](/case-studies/2026-04-24-shanraisshan-claude-code-best-practice).

- **Per-repo report**: [/reports/shanraisshan-claude-code-best-practice](/reports/shanraisshan-claude-code-best-practice)
- **Merged PRs**: [#63](https://github.com/shanraisshan/claude-code-best-practice/pull/63) · [#65](https://github.com/shanraisshan/claude-code-best-practice/pull/65) · [#66](https://github.com/shanraisshan/claude-code-best-practice/pull/66) · [#67](https://github.com/shanraisshan/claude-code-best-practice/pull/67)
- **Repo**: <https://github.com/shanraisshan/claude-code-best-practice>

## 6. safishamsi/graphify

37,391 stars. Audit score 58/100, security REVIEW. One merged PR — the [case study](/case-studies/2026-05-03-safishamsi-graphify) documents both what we fixed and the high-confidence reproduction discipline that earned the contribute step's trust on a low-scoring repo.

- **Per-repo report**: [/reports/safishamsi-graphify](/reports/safishamsi-graphify)
- **Merged PRs**: [#603](https://github.com/safishamsi/graphify/pull/603)
- **Repo**: <https://github.com/safishamsi/graphify>

## 7. luongnv89/claude-howto

27,150 stars. Audit score 77/100, security REVIEW. Three merged PRs — broken references and missing fields. [Case study](/case-studies/2026-04-25-luongnv89-claude-howto).

- **Per-repo report**: [/reports/luongnv89-claude-howto](/reports/luongnv89-claude-howto)
- **Merged PRs**: [#89](https://github.com/luongnv89/claude-howto/pull/89) · [#90](https://github.com/luongnv89/claude-howto/pull/90) · [#91](https://github.com/luongnv89/claude-howto/pull/91)
- **Repo**: <https://github.com/luongnv89/claude-howto>

## 8. K-Dense-AI/scientific-agent-skills

19,356 stars. Audit score 83/100, security CLEAR. Four merged PRs — the highest contribute-step yield on a single repo with no case study (the engagement was straightforward enough to skip the long-form article).

- **Per-repo report**: [/reports/K-Dense-AI-scientific-agent-skills](/reports/K-Dense-AI-scientific-agent-skills)
- **Merged PRs**: [#145](https://github.com/K-Dense-AI/scientific-agent-skills/pull/145) · [#146](https://github.com/K-Dense-AI/scientific-agent-skills/pull/146) · [#147](https://github.com/K-Dense-AI/scientific-agent-skills/pull/147) · [#149](https://github.com/K-Dense-AI/scientific-agent-skills/pull/149)
- **Repo**: <https://github.com/K-Dense-AI/scientific-agent-skills>

## 9. mukul975/Anthropic-Cybersecurity-Skills

4,317 stars. Audit score 79/100, security REVIEW. One merged PR. Notable because the repo's domain (security skills for Claude) overlaps with NLPM's own security-scanner — a natural fit for the auditor's coverage.

- **Per-repo report**: [/reports/mukul975-Anthropic-Cybersecurity-Skills](/reports/mukul975-Anthropic-Cybersecurity-Skills)
- **Merged PRs**: [#44](https://github.com/mukul975/Anthropic-Cybersecurity-Skills/pull/44)
- **Repo**: <https://github.com/mukul975/Anthropic-Cybersecurity-Skills>

## 10. gotalab/cc-sdd

3,099 stars. Audit score 60/100, security CLEAR. Three merged PRs paired with a [case study](/case-studies/2026-04-27-gotalab-cc-sdd). A clean example of how a low initial score becomes a positive engagement after concrete fixes are accepted.

- **Per-repo report**: [/reports/gotalab-cc-sdd](/reports/gotalab-cc-sdd)
- **Merged PRs**: [#166](https://github.com/gotalab/cc-sdd/pull/166) · [#169](https://github.com/gotalab/cc-sdd/pull/169) · [#170](https://github.com/gotalab/cc-sdd/pull/170)
- **Repo**: <https://github.com/gotalab/cc-sdd>

## See also

- [NLPM self-audit](/reports/xiaolai-nlpm-for-claude) — NLPM at 100/100 against its own rule set
- [Full dashboard](/dashboard) — every audited repo, sortable
- [Case studies](/case-studies/) — long-form articles, 29 total
- [Framework reference](/reference/) — the rules, principles, and vocabulary that produced these findings
