# Re-Audit: safishamsi/graphify

**Date**: 2026-05-03  |  **Before**: `eceaaad` (58/100)  |  **After**: `893acb1` (100/100)

## Summary

| Outcome | Count |
|---------|------:|
| fixed — our PR merged | 1 |
| fixed — upstream, not via our PR | 11 |

## Original findings — verification

| # | File | Line | Rule | Pattern | Outcome | PR |
|---|------|------|------|---------|---------|----|
| 1 | `graphify/skill-trae.md` | 829 | BUG-syntax-error | `python-dict-literal-typo` | fixed — our PR merged | #603 |
| 2 | `graphify/skill.md` | 80 | BUG-path-mismatch | `interpreter-cache-path-drift` | fixed — upstream, not via our PR |  |
| 3 | `graphify/skill-vscode.md` | 154 | BUG-empty-loop-placeholder | `empty-iteration-placeholder` | fixed — upstream, not via our PR |  |
| 4 | `graphify/skill.md` | — | R09 | `missing-example-blocks` | fixed — upstream, not via our PR |  |
| 5 | `graphify/skill.md` | — | R03 | `missing-version-field` | fixed — upstream, not via our PR |  |
| 6 | `graphify/skill.md` | — | R12 | `non-canonical-skill-path` | fixed — upstream, not via our PR |  |
| 7 | `graphify/skill-copilot.md` | — | CC-duplicate-variants | `redundant-variant` | fixed — upstream, not via our PR |  |
| 8 | `graphify/skill-aider.md` | — | CC-stale-variant | `feature-drift-from-canonical` | fixed — upstream, not via our PR |  |
| 9 | `graphify/__main__.py` | 922 | SEC-allowlist-bypass | `loose-url-regex` | fixed — upstream, not via our PR |  |
| 10 | `graphify/__main__.py` | 948 | SEC-path-traversal | `unbounded-output-path` | fixed — upstream, not via our PR |  |
| 11 | `graphify/security.py` | 52 | SEC-ssrf-blocklist-narrow | `incomplete-metadata-blocklist` | fixed — upstream, not via our PR |  |
| 12 | `pyproject.toml` | 13 | SEC-unpinned-deps | `no-version-pins` | fixed — upstream, not via our PR |  |

