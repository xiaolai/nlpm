# NLPM Audit: IvanMurzak/Unity-MCP
**Date**: 2026-04-12  |  **Artifacts**: 78  |  **Strategy**: progressive
**NL Score**: 82/100
**Security**: CLEAR
**Bugs**: 9  |  **Quality Issues**: 22  |  **Security Findings**: 5

## NL Score Summary
| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| `.claude/commands/speckit.taskstoissues.md` | command | 60 | Missing `name` frontmatter; no example blocks |
| `.claude/commands/speckit.analyze.md` | command | 65 | Missing `name` frontmatter; no `allowed-tools` |
| `.claude/commands/speckit.checklist.md` | command | 65 | Missing `name` frontmatter; no `allowed-tools` |
| `.claude/commands/speckit.clarify.md` | command | 65 | Missing `name` frontmatter; no `allowed-tools` |
| `.claude/commands/speckit.constitution.md` | command | 65 | Missing `name` frontmatter; no `allowed-tools` |
| `.claude/commands/speckit.implement.md` | command | 65 | Missing `name` frontmatter; no `allowed-tools` |
| `.claude/commands/speckit.plan.md` | command | 65 | Missing `name` frontmatter; no `allowed-tools` |
| `.claude/commands/speckit.specify.md` | command | 65 | Missing `name` frontmatter; no `allowed-tools` |
| `.claude/commands/speckit.tasks.md` | command | 65 | Missing `name` frontmatter; no `allowed-tools` |
| `CLAUDE.md` | context | 75 | No frontmatter by design; startup flow omits tool constraints |
| `Unity-MCP-Plugin/CLAUDE.md` | context | 75 | No frontmatter by design; testing patterns lack concrete examples |
| `Unity-MCP-Plugin/.claude/skills/editor-selection-get/SKILL.md` | skill | 76 | All 6 boolean input parameters have empty descriptions |
| `Unity-MCP-Server/CLAUDE.md` | context | 78 | No frontmatter by design; webhook config tables thorough but no examples |
| `Unity-MCP-Plugin/.claude/skills/scene-set-active/SKILL.md` | skill | 80 | `sceneRef` description uses generic AssetObjectRef text ("Material, ScriptableObject, Prefab…") instead of scene-specific text |
| `Unity-MCP-Plugin/.claude/skills/assets-refresh/SKILL.md` | skill | 83 | No output section; no model declaration |
| `Unity-MCP-Plugin/.claude/skills/assets-prefab-save/SKILL.md` | skill | 83 | No output section; no model declaration |
| `Unity-MCP-Plugin/.claude/skills/assets-shader-get-data/SKILL.md` | skill | 83 | Table types `any` for boolean params; schema shows `System.Boolean` — type mismatch |
| `Unity-MCP-Plugin/.claude/skills/console-clear-logs/SKILL.md` | skill | 83 | No output section; no model declaration |
| `Unity-MCP-Plugin/.claude/skills/ping/SKILL.md` | skill | 83 | No output section; no model declaration |
| `Unity-MCP-Plugin/.claude/skills/scene-save/SKILL.md` | skill | 83 | No output section; no model declaration |
| `Unity-MCP-Plugin/.claude/skills/screenshot-camera/SKILL.md` | skill | 83 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/screenshot-game-view/SKILL.md` | skill | 83 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/screenshot-scene-view/SKILL.md` | skill | 83 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/tool-list/SKILL.md` | skill | 83 | `includeDescription` and `includeInputs` typed as `any` in parameter table |
| `Unity-MCP-Plugin/.claude/skills/assets-copy/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-create-folder/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-delete/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-find/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-find-built-in/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-get-data/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-material-create/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-modify/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-move/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-prefab-close/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-prefab-create/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-prefab-instantiate/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-prefab-open/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/assets-shader-list-all/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/console-get-logs/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/editor-application-get-state/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/editor-application-set-state/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/editor-selection-set/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-component-add/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-component-destroy/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-component-get/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-component-list-all/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-component-modify/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-create/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-destroy/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-duplicate/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-find/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-modify/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/gameobject-set-parent/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/object-get-data/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/object-modify/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/package-add/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/package-list/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/package-remove/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/package-search/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/reflection-method-call/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/reflection-method-find/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/scene-create/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/scene-get-data/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/scene-list-opened/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/scene-open/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/scene-unload/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/script-delete/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/script-execute/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/script-read/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/script-update-or-create/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/tests-run/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/tool-set-enabled-state/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/type-get-json-schema/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/unity-initial-setup/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `Unity-MCP-Plugin/.claude/skills/unity-skill-generate/SKILL.md` | skill | 85 | No model declaration; no `allowed-tools` |
| `.claude/skills/github-pr-review-fix/SKILL.md` | skill | 88 | Minor: no `model` declaration |
| `.claude/skills/build-cli/SKILL.md` | skill | 90 | None |
| `Unity-MCP-Plugin/.claude/skills/unity-skill-create/SKILL.md` | skill | 90 | None — exemplary; includes C# code sample and pattern documentation |

## Security Scan
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 2 |

### Execution Surface Inventory
| Surface | Files |
|---------|-------|
| Hooks | None |
| Scripts (bash) | `Unity-MCP-Server/build-all.sh` |
| Scripts (PowerShell) | `commands/bump-version.ps1`, `commands/generate-release.ps1`, `commands/run-act-test.ps1`, `commands/run-unity-tests.ps1`, `commands/update-unity-mcp-server.ps1`, `.specify/scripts/powershell/check-prerequisites.ps1`, `.specify/scripts/powershell/common.ps1`, `.specify/scripts/powershell/create-new-feature.ps1`, `.specify/scripts/powershell/setup-plan.ps1`, `.specify/scripts/powershell/update-agent-context.ps1` |
| MCP configs | None (server binary managed by plugin; no `.mcp.json` at repo root) |
| Package manifests | `cli/package.json`, `cli/package-lock.json`, `Unity-MCP-Server/com.IvanMurzak.Unity.MCP.Server.csproj` |
| Runtime download | `Library/mcp-server/{platform}/` — binary downloaded from GitHub releases on plugin startup (`McpServerManager.cs`) |

### Security Findings
| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | Medium | `commands/run-act-test.ps1` | 171–233 | `Invoke-Expression` with dynamically-built string | `$actCommand` is assembled by string concatenation from `$JobName`, `$WorkflowFile`, and raw secret values read from a `.env` file, then passed to `Invoke-Expression`. If the `.env` file contains values with embedded PowerShell metacharacters (e.g., `$(...)`, semicolons, backticks), the expression could be widened beyond intent. In a developer-only local tool this is Low severity in practice, but the `Invoke-Expression` pattern itself is a code-injection surface. Replace with `Start-Process act` with an explicit argument array. |
| 2 | Medium | `commands/generate-release.ps1` | 13–15, 45–46 | Unauthenticated external network call | `gh api "repos/$repoPath/commits/$sha"` is called for every commit without verifying the `gh` CLI is authenticated or that `$repoPath` is the expected repo. If `origin` is tampered (e.g., via `git remote set-url`), the script will call the GitHub API for an attacker-controlled repo. Additionally, commit data returned by the API is embedded directly into a markdown file without HTML-escaping — a content-injection risk if the release notes file is later rendered. |
| 3 | Medium | Plugin startup (`McpServerManager.cs` per CLAUDE.md) | N/A | Runtime binary download without integrity verification | The plugin downloads a self-contained server executable from GitHub releases to `Library/mcp-server/{platform}/` on every version change. The CLAUDE.md documents only a `version` file for tracking; no checksum or signature verification is described. A man-in-the-middle attack on the GitHub release download URL (or a compromised GitHub release) would silently replace the server binary with a malicious one that runs in the Unity Editor context. |
| 4 | Low | `commands/update-unity-mcp-server.ps1` | 103–113 | Unpinned NuGet dependency resolution | `dotnet add $fullPath package $package` resolves to the latest available version on NuGet at execution time. This means `com.IvanMurzak.ReflectorNet` and `com.IvanMurzak.McpPlugin.Server` can change unexpectedly between runs. Pinned version strings in the `.csproj` are discarded each run. |
| 5 | Low | `commands/run-act-test.ps1` | 115–147 | Credentials stored in plaintext `.env` file | `UNITY_LICENSE`, `UNITY_EMAIL`, and `UNITY_PASSWORD` are read from `commands/.env`. The script checks for its existence but does not verify file permissions. A world-readable `.env` file (the default on most Unix systems) exposes Unity account credentials to any local process. The `.env` file is presumably gitignored, but this is not enforced by the script. |

## Bugs (PR-worthy)
| # | File | Issue | Impact |
|---|------|-------|--------|
| 1 | `.claude/commands/speckit.taskstoissues.md` | Missing `name` frontmatter field. The `tools` array is present but `name` is absent, preventing Claude Code from correctly registering and displaying the command identity. | Claude Code may silently drop or misidentify this command in the command palette. |
| 2 | `.claude/commands/speckit.analyze.md` | Missing `name` frontmatter field. Only `description` and `handoffs` are present. | Same registration failure as bug #1. |
| 3 | `.claude/commands/speckit.checklist.md` | Missing `name` frontmatter field. Only `description` is present. | Same registration failure as bug #1. |
| 4 | `.claude/commands/speckit.clarify.md` | Missing `name` frontmatter field. Only `description` and `handoffs` are present. | Same registration failure as bug #1. |
| 5 | `.claude/commands/speckit.constitution.md` | Missing `name` frontmatter field. Only `description` and `handoffs` are present. | Same registration failure as bug #1. |
| 6 | `.claude/commands/speckit.implement.md` | Missing `name` frontmatter field. Only `description` is present. | Same registration failure as bug #1. |
| 7 | `.claude/commands/speckit.plan.md` | Missing `name` frontmatter field. Only `description` and `handoffs` are present. | Same registration failure as bug #1. |
| 8 | `.claude/commands/speckit.specify.md` | Missing `name` frontmatter field. Only `description` and `handoffs` are present. | Same registration failure as bug #1. |
| 9 | `.claude/commands/speckit.tasks.md` | Missing `name` frontmatter field. Only `description` and `handoffs` are present. | Same registration failure as bug #1. |

## Security Fixes (PR-worthy, Medium/Low only)
| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | `commands/run-act-test.ps1` | `Invoke-Expression $actCommand` executes a dynamically-assembled string, enabling argument/command injection via `.env` values or parameter inputs. | Replace `Invoke-Expression "$actCommand ..."` with `$actArgs = @('-j', $JobName, '-W', $WorkflowFile, ...)` and `& act @actArgs`. This avoids shell parsing entirely. Validate `$JobName` and `$WorkflowFile` with an allowlist or simple regex before use. |
| 2 | `commands/generate-release.ps1` | Commit data from `gh api` is interpolated directly into a markdown file without sanitization; `origin` URL is trusted without validation. | (a) Validate `$repoUrl` against the expected owner/repo before making API calls. (b) HTML-encode or markdown-escape the `$message` value before writing it to the output file to prevent content injection. |
| 3 | Plugin startup (`McpServerManager.cs`) | Server binary downloaded from GitHub releases with no checksum or signature verification. | After downloading, verify the binary SHA256 against a known-good hash published in the release manifest (or a separate `.sha256` file in the release assets). Reject and delete the binary if the hash does not match before executing. |
| 4 | `commands/update-unity-mcp-server.ps1` | Latest-version NuGet resolution replaces pinned versions silently. | Accept an optional `-Version` parameter for each package. When omitted, print the resolved version and require `--confirm` or a separate commit step, rather than silently overwriting the `.csproj`. |
| 5 | `commands/run-act-test.ps1` | `.env` file with Unity credentials has no permission enforcement. | Add `(Get-Item $envFile).Attributes` check (Windows) or `stat` equivalent (Linux/macOS via `[System.IO.File]::GetAccessControl`) and warn if the file is readable by other users. Document in `.env.example` that the file must be owner-read-only. |

## Quality Issues (informational)
| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | All 9 `speckit.*` commands | No `model` frontmatter field — model selection left to runtime default rather than declared intent | -5 each |
| 2 | 7 `speckit.*` commands (all except `speckit.taskstoissues`) | No `allowed-tools` (or `tools`) frontmatter field — tool permission boundary undeclared | -5 each |
| 3 | `Unity-MCP-Plugin/.claude/skills/editor-selection-get/SKILL.md` | All 6 boolean input parameters (`includeInactive`, `includePrefabStage`, `returnMultiple`, `showInHierarchy`, `includeHiddenObjects`, `includeChildObjects`) have empty `Description` column entries in the input table — AI has no guidance on what each flag controls | -2 each (×6) |
| 4 | `Unity-MCP-Plugin/.claude/skills/scene-set-active/SKILL.md` | `sceneRef` input description reads "Material, ScriptableObject, Prefab…" — this is the generic `AssetObjectRef` boilerplate, wrong for a scene-reference parameter. The description should identify valid scene path formats. | -2 |
| 5 | `Unity-MCP-Plugin/.claude/skills/assets-shader-get-data/SKILL.md` | `includeBuiltIn` and `includeHidden` optional params are typed as `any` in the parameter table but declared as `System.Boolean` in the JSON Schema — type mismatch confuses callers | -2 each |
| 6 | `Unity-MCP-Plugin/.claude/skills/tool-list/SKILL.md` | `includeDescription` and `includeInputs` parameters typed as `any` in the table; schema uses `System.Boolean` — same type-mismatch pattern | -2 each |
| 7 | All 64 plugin skills in `Unity-MCP-Plugin/.claude/skills/` | No `model` frontmatter field — these are read-only API reference docs so impact is low, but the pattern is inconsistent with root skills | -5 each (systemic) |
| 8 | All 64 plugin skills in `Unity-MCP-Plugin/.claude/skills/` | No `allowed-tools` frontmatter field — API reference docs, so low practical impact, but pattern differs from root skills | -5 each (systemic) |

## Cross-Component
- **speckit ↔ scripts**: All 9 speckit commands invoke `.specify/scripts/powershell/check-prerequisites.ps1`, `common.ps1`, and related scripts. Those scripts exist and the `Get-FeaturePathsEnv` / `Test-FeatureBranch` functions referenced by `check-prerequisites.ps1` are implemented in `common.ps1`. Cross-reference is intact.
- **build-cli skill ↔ CLI source**: `.claude/skills/build-cli/SKILL.md` references the `cli/` directory. `cli/package.json` exists. Reference is valid.
- **github-pr-review-fix skill ↔ GitHub MCP**: `.claude/skills/github-pr-review-fix/SKILL.md` uses `disable-model-invocation: true` and references sub-agent patterns. No broken tool references found.
- **plugin skills ↔ MCP tool registry**: All 64 plugin skills in `Unity-MCP-Plugin/.claude/skills/` correspond to MCP tool names registered via `[McpPluginTool]` attributes (per plugin CLAUDE.md conventions). The tool names follow the `category-action` kebab-case pattern documented in the root CLAUDE.md. No orphaned skill files detected.
- **version files**: `commands/bump-version.ps1` lists 7 version file locations. All 7 paths exist: `Unity-MCP-Server/server.json`, `Unity-MCP-Server/com.IvanMurzak.Unity.MCP.Server.csproj`, `Installer/Assets/com.IvanMurzak/AI Game Dev Installer/Installer.cs`, `Unity-MCP-Plugin/Assets/root/package.json`, `Unity-MCP-Plugin/Assets/root/Runtime/UnityMcpPlugin.cs`, `cli/package.json`, `cli/src/utils/manifest.ts`. Bump script is consistent with repo layout.
- **README sync**: Root CLAUDE.md documents that `Unity-MCP-Plugin/Assets/root/README.md` and `Installer/Assets/.../README.md` MUST stay in sync with `README.md`. No automated enforcement exists — this is a manual process. Risk of drift.

## Recommendation
**Fix bugs first (9 PRs or 1 batch PR)**: All 9 speckit commands are missing the `name` frontmatter field. This is a one-line fix per file but critical — Claude Code uses `name` for command registration and user-facing display. A single PR adding the correct `name` to each file's frontmatter unblocks correct behaviour for the entire speckit workflow suite.

**Address security finding #3 (binary integrity)**: The runtime download of self-contained server executables from GitHub releases without checksum verification is the highest-risk security pattern in this repo. It runs silently in the Unity Editor context. Adding SHA256 verification before execution (with a companion `.sha256` file in the release assets) would close this attack surface at low implementation cost.

**Fix type mismatches in 3 plugin skill parameter tables**: `assets-shader-get-data`, `tool-list`, and `editor-selection-get` all have incorrect or missing parameter descriptions that will mislead AI callers. These are documentation-only fixes with no code changes required.

**Replace `Invoke-Expression` in run-act-test.ps1**: Switching from `Invoke-Expression $actCommand` to `& act @actArgs` (splatted argument array) is a 10-line refactor that eliminates the command-injection surface entirely.

**Systemic quality improvement**: The 64 plugin skills and 9 commands all lack `model` and `allowed-tools` frontmatter. Adding these in bulk (via a script or templated PR) would raise the overall NL Score from 82 to approximately 90 and make tool permission boundaries explicit — particularly valuable for the reflection and script-execution tools which have elevated Unity Editor access.
