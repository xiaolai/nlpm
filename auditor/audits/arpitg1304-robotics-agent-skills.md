# NLPM Audit: arpitg1304/robotics-agent-skills
**Date**: 2026-04-06  |  **Artifacts**: 10  |  **Strategy**: single
**NL Score**: 74/100
**Security**: REVIEW
**Bugs**: 2  |  **Quality Issues**: 38  |  **Security Findings**: 1

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/ros2/SKILL.md | Skill | 60 | `name: ros2-development` doesn't match parent dir `ros2` (-15) |
| skills/ros1/SKILL.md | Skill | 70 | `name: ros1-development` doesn't match parent dir `ros1` (-15) |
| skills/robot-bringup/SKILL.md | Skill | 73 | Description >800 chars (R04, -10) |
| skills/robot-perception/SKILL.md | Skill | 73 | Description >800 chars (R04, -10) |
| skills/docker-ros2-development/SKILL.md | Skill | 75 | Description >800 chars (R04, -10) |
| skills/robotics-security/SKILL.md | Skill | 75 | Description >800 chars (R04, -10) |
| skills/robotics-software-principles/SKILL.md | Skill | 75 | Description >800 chars (R04, -10) |
| skills/ros2-web-integration/SKILL.md | Skill | 75 | Description >800 chars (R04, -10) |
| skills/robotics-design-patterns/SKILL.md | Skill | 82 | Body >500 lines (R05, -10) |
| skills/robotics-testing/SKILL.md | Skill | 82 | Body >500 lines (R05, -10) |

All 10 artifacts are Claude Code Tier-1 (open-spec) `SKILL.md` files — no agents, commands, or hooks are present in this repository. Every file has valid `name`/`description` frontmatter, extensive runnable (non-pseudocode) examples, and no vague-quantifier problems beyond a handful of isolated words. The score drag is structural: every file exceeds the 500-line body budget (or, for `ros1`, the 400-line band), every description is long enough to hit the R04 length penalty, none of the 10 files cross-reference any of the other 9 despite heavy topical overlap (no R07 scope notes), and two files have a `name:` field that does not match their parent directory.

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 0 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | 0 files |
| Scripts | 11 files: `install.sh`; `evals/with-skills/demo_recorder/{setup.py, demo_recorder/__init__.py, demo_recorder/demo_recorder_node.py, demo_recorder/episode_writer.py, launch/demo_recorder.launch.py, test/test_demo_recorder.py}`; `evals/without-skills/demo_recorder/{setup.py, demo_recorder/__init__.py, demo_recorder/demo_recorder_node.py, launch/demo_recorder.launch.py}` |
| MCP configs | 0 files |
| Package manifests | 0 files (no `package.json`/`requirements.txt` at repo root; ROS2 `package.xml`/`setup.py` are colcon manifests, not scanned as dependency manifests) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|--------------|
| 1 | Medium | install.sh | 76-87 | SEC-path-traversal | `--skills` values are interpolated directly into `rm -rf "${target}/${skill}"` and `cp -R "${src}" "${target}/${skill}"` with no validation (e.g. no `^[A-Za-z0-9_-]+$` check). A skill argument containing `../` (e.g. `--skills ../../etc`) that happens to resolve to an existing directory under `skills_dir`'s parent tree would cause the script to `rm -rf` and overwrite a path outside the intended target directory. |

All 10 `evals/**/*.py` files were reviewed for `eval`/`exec`, `subprocess`/`os.system`, `shell=True`, network calls, hardcoded credentials, and unsafe deserialization — none found. They are inert ROS2 example nodes (rclpy lifecycle node, launch files, pytest suite) with no execution-surface risk beyond normal ROS2 node behavior.

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | skills/ros1/SKILL.md | Frontmatter `name: ros1-development` does not match parent directory `ros1` | Violates the open Agent Skills spec (agentskills.io) MUST requirement; tooling that derives skill identity from `name:` (rather than directory) will register/reference this skill under a different name than its path, breaking lookups keyed by directory |
| 2 | skills/ros2/SKILL.md | Frontmatter `name: ros2-development` does not match parent directory `ros2` | Same as above |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|----------------|
| 1 | install.sh | Unsanitized `--skills` argument used in `rm -rf`/`cp -R` (path traversal) | Validate each skill token against `^[A-Za-z0-9_-]+$` before use, or resolve `realpath` on `${src}` and confirm the result is still inside `${skills_dir}` before touching `${target}/${skill}` |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | skills/docker-ros2-development/SKILL.md | Description length >800 chars (R04) | -10 |
| 2 | skills/docker-ros2-development/SKILL.md | Body 1102 lines, exceeds 500-line budget (R05) | -10 |
| 3 | skills/docker-ros2-development/SKILL.md | No scope note / cross-references to sibling skills (R07) | -3 |
| 4 | skills/docker-ros2-development/SKILL.md | Vague quantifier: "appropriate" (line 1000), 1 occurrence (R01) | -2 |
| 5 | skills/robot-bringup/SKILL.md | Description length >800 chars (R04) | -10 |
| 6 | skills/robot-bringup/SKILL.md | Body 1806 lines, exceeds 500-line budget (R05) | -10 |
| 7 | skills/robot-bringup/SKILL.md | No scope note / cross-references (R07) | -3 |
| 8 | skills/robot-bringup/SKILL.md | Vague quantifiers: "correctly" x2 (lines 24, 1805) (R01) | -4 |
| 9 | skills/robot-perception/SKILL.md | Description length >800 chars (R04) | -10 |
| 10 | skills/robot-perception/SKILL.md | Body 1654 lines, exceeds 500-line budget (R05) | -10 |
| 11 | skills/robot-perception/SKILL.md | No scope note / cross-references (R07) | -3 |
| 12 | skills/robot-perception/SKILL.md | Vague quantifiers: "various" (line 110), "sufficient" (line 285) (R01) | -4 |
| 13 | skills/robotics-design-patterns/SKILL.md | Description length 500-800 chars (R04) | -5 |
| 14 | skills/robotics-design-patterns/SKILL.md | Body 609 lines, exceeds 500-line budget (R05) | -10 |
| 15 | skills/robotics-design-patterns/SKILL.md | No scope note / cross-references (R07) | -3 |
| 16 | skills/robotics-security/SKILL.md | Description length >800 chars (R04) | -10 |
| 17 | skills/robotics-security/SKILL.md | Body 890 lines, exceeds 500-line budget (R05) | -10 |
| 18 | skills/robotics-security/SKILL.md | No scope note / cross-references (R07) | -3 |
| 19 | skills/robotics-security/SKILL.md | Vague quantifier: "sufficient" (line 494) (R01) | -2 |
| 20 | skills/robotics-software-principles/SKILL.md | Description length >800 chars (R04) | -10 |
| 21 | skills/robotics-software-principles/SKILL.md | Body 896 lines, exceeds 500-line budget (R05) | -10 |
| 22 | skills/robotics-software-principles/SKILL.md | No scope note / cross-references (R07) | -3 |
| 23 | skills/robotics-software-principles/SKILL.md | Vague quantifier: "some" (line 27) (R01) | -2 |
| 24 | skills/robotics-testing/SKILL.md | Description length 500-800 chars (R04) | -5 |
| 25 | skills/robotics-testing/SKILL.md | Body 577 lines, exceeds 500-line budget (R05) | -10 |
| 26 | skills/robotics-testing/SKILL.md | No scope note / cross-references (R07) | -3 |
| 27 | skills/ros1/SKILL.md | Description length 500-800 chars (R04) | -5 |
| 28 | skills/ros1/SKILL.md | Body 407 lines, in 400-500 band (R05) | -5 |
| 29 | skills/ros1/SKILL.md | No scope note / cross-references (R07) | -3 |
| 30 | skills/ros1/SKILL.md | Vague quantifier: "correctly" (line 171) (R01) | -2 |
| 31 | skills/ros2-web-integration/SKILL.md | Description length >800 chars (R04) | -10 |
| 32 | skills/ros2-web-integration/SKILL.md | Body 1430 lines, exceeds 500-line budget (R05) | -10 |
| 33 | skills/ros2-web-integration/SKILL.md | No scope note / cross-references (R07) | -3 |
| 34 | skills/ros2-web-integration/SKILL.md | Vague quantifier: "properly" (line 1426) (R01) | -2 |
| 35 | skills/ros2/SKILL.md | Description length >800 chars (R04) | -10 |
| 36 | skills/ros2/SKILL.md | Body 994 lines, exceeds 500-line budget (R05) | -10 |
| 37 | skills/ros2/SKILL.md | No scope note / cross-references (R07) | -3 |
| 38 | skills/ros2/SKILL.md | Vague quantifier: "some" (line 315) (R01) | -2 |

## Cross-Component
No broken references found. `README.md`'s skill table, recommended bundles, and coverage map all resolve to the 10 existing `skills/*/SKILL.md` directories, and the `![skills-10]` badge matches the actual count. `install.sh`'s `default_skills` array (`ros2 robotics-software-principles robotics-testing robot-bringup`) and its `--list`/`--skills all` logic (`find "${skills_dir}" -mindepth 1 -maxdepth 1 -type d`) both resolve correctly against the real directory set. No orphaned skill files and no contradictions between skills were found.

The one structural gap worth flagging as a pattern (not a single-file bug): none of the 10 skills cross-reference each other despite clear topical adjacency — e.g. `ros1` and `ros2` cover overlapping middleware ground, `robot-bringup` and `docker-ros2-development` both discuss systemd/entrypoint sourcing, and `robotics-security` and `robot-bringup` both discuss network/firewall configuration. A "Scope Note" or "See also" section in each file pointing to the others would resolve the ten individual R07 findings at once.

## Recommendation
REVIEW — submit NL fix PRs (the two `name:`/directory mismatches are high-confidence, single-line diffs), and flag the `install.sh` path-traversal finding in the audit issue rather than opening a public PR outright given it touches a file-deletion code path — a maintainer should confirm the intended fix before a PR lands.
