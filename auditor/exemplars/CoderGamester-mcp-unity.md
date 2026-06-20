---
slug: CoderGamester-mcp-unity
repo: CoderGamester/mcp-unity
audited: 2026-06-20
commit_sha: cce8b57de9cb69633deb222c9162dad539a52b87
score: 90
exemplifies:
  - R06
  - R33
  - R34
  - R35
  - R38
---

# Exemplar: CoderGamester/mcp-unity

**Score**: 90/100  |  **Date**: 2026-06-20  |  **Commit**: `cce8b57de9cb69633deb222c9162dad539a52b87`

A single-artifact CLAUDE.md for a two-tier MCP bridge (Unity C# ↔ Node.js TypeScript) that demonstrates how to write a project memory file that instructs rather than describes: runnable examples, exact commands with caveats noted, annotated directory trees, and a pitfall list grounded in real failure modes.

## Per-rule evidence

### R33 — Include build/run command

The "Build & Development Commands" section covers both tiers of the architecture, each in its own labelled bash block with inline annotations explaining non-obvious commands.

> Real quote from `CLAUDE.md:15-25`:
>
> ```
> ## Build & Development Commands
>
> ### Node.js Server (`Server~/`)
> ```bash
> npm install          # Install dependencies
> npm run build        # Compile TypeScript to build/
> npm run watch        # Watch mode compilation
> npm start            # Run server (node build/index.js)
> npm test             # Run Jest tests (uses --experimental-vm-modules)
> npm run test:watch   # Watch mode testing
> npm run inspector    # Launch MCP Inspector for debugging
> ```
>
> ### Unity Side
> - Build/Test via Unity Editor
> - **Tools > MCP Unity > Server Window** for configuration
> - **Window > General > Test Runner** for EditMode tests
> ```

The inline comment on `npm test` (`uses --experimental-vm-modules`) is what distinguishes this from a generic command list — it flags the non-obvious flag so an agent doesn't strip it when regenerating a test invocation.

### R34 — Include test command

Both test paths are covered: `npm test` for the Node side and the exact Editor menu path for the Unity side, so a contributor can verify changes on either tier without guessing.

> Real quote from `CLAUDE.md:22-24`:
>
> ```
> npm test             # Run Jest tests (uses --experimental-vm-modules)
> npm run test:watch   # Watch mode testing
> ```

And for Unity:

> Real quote from `CLAUDE.md:30`:
>
> ```
> - **Window > General > Test Runner** for EditMode tests
> ```

Two test surfaces, two distinct commands. The `test:watch` alias covers the iteration loop that an agent running repeated edits would use.

### R35 — Include architecture overview

The "Key Directories" section is an annotated ASCII tree that goes two levels deep, naming each leaf and its role. A reader can map any file path to its architectural purpose without opening the code.

> Real quote from `CLAUDE.md:33-49`:
>
> ```
> ## Key Directories
>
> ```
> Editor/                       # Unity Editor package (C#)
> ├── Tools/                    # MCP tools (inherit McpToolBase)
> ├── Resources/                # MCP resources (inherit McpResourceBase)
> ├── Services/                 # TestRunnerService, ConsoleLogsService
> ├── UnityBridge/              # WebSocket server + message routing
> │   ├── McpUnityServer.cs     # Singleton managing server lifecycle
> │   └── McpUnitySocketHandler.cs  # WebSocket handler
> └── Utils/                    # Logging, config, workspace helpers
>
> Server~/                      # Node.js MCP server (TypeScript/ESM)
> ├── src/index.ts              # Entry point - registers tools/resources
> ├── src/tools/                # MCP tool definitions (zod + handler)
> ├── src/resources/            # MCP resource definitions
> └── src/unity/mcpUnity.ts     # WebSocket client connecting to Unity
> ```
> ```

The tree also labels the architectural role (e.g., "Singleton managing server lifecycle"), not just the technical fact. That turns directory browsing into component comprehension.

### R06 — Code examples must be runnable

The "Adding a New Tool" section gives a three-step walkthrough with a real C# class and a real TypeScript function — not pseudocode, and not a description of what to write.

> Real quote from `CLAUDE.md:58-83`:
>
> ```
> ## Adding a New Tool
>
> ### 1. Unity Side (C#)
> Create `Editor/Tools/YourTool.cs`:
> ```csharp
> public class YourTool : McpToolBase {
>     public override string Name => "your_tool";  // Must match Node side
>     public override JObject Execute(JObject parameters) {
>         // Implementation
>     }
> }
> ```
> Register in `McpUnityServer.cs` → `RegisterTools()`.
>
> ### 2. Node Side (TypeScript)
> Create `Server~/src/tools/yourTool.ts`:
> ```typescript
> export function registerYourTool(server: McpServer, mcpUnity: McpUnity, logger: Logger) {
>   server.tool("your_tool", "Description", paramsSchema.shape, async (params) => {
>     return await mcpUnity.sendRequest({ method: "your_tool", params });
>   });
> }
> ```
> Register in `Server~/src/index.ts`.
>
> ### 3. Build
> ```bash
> cd Server~ && npm run build
> ```
> ```

The C# and TypeScript stubs use real method signatures (`McpToolBase`, `JObject`, `McpServer`, `McpUnity`, `Logger`) and the inline comment `// Must match Node side` cross-references the constraint stated in "Key Invariants". A contributor can copy-paste and compile.

### R38 — More instructive than descriptive

The file allocates its tokens to: exact commands, a runnable extension pattern, a pitfall list with named failure modes, and configuration fields with defaults. The "Project Overview" section is the only descriptive passage, and it spans 6 lines before the file switches to instruction.

> Real quote from `CLAUDE.md:111-119`:
>
> ```
> ## Common Pitfalls
>
> - **Name mismatch**: Node tool/resource name must equal Unity `Name` exactly
> - **Long main-thread work**: Synchronous `Execute()` blocks Unity; use `IsAsync = true` with `ExecuteAsync()` for long operations
> - **Unity domain reload**: Server stops during script reloads; avoid persistent in-memory state
> - **Port conflicts**: Default is 8090; check if another process is using it
> - **Multiplayer Play Mode**: Clone instances auto-skip server startup; only main editor hosts MCP
> ```

Each pitfall names the failure mode and the fix in one line. No abstract advice — every entry would catch a real bug.

## Worth adopting

Pattern: **Key Invariants section for cross-cutting constraints**. Evidence: `CLAUDE.md:51-57`. The file dedicates a separate `## Key Invariants` section to the constraints that govern all tools and resources simultaneously (naming convention, execution thread, config file path, WebSocket endpoint). These constraints are not build steps, not architecture, and not rules — they are operating assumptions an agent must not violate. The current R33–R39 set covers build, test, architecture, and freshness, but not a slot for "these facts are always true regardless of which file you're editing." A rule of the form: **State load-bearing invariants in a dedicated section.** Facts that, if wrong, silently break inter-component contracts should be listed in one place, not scattered across subsections where they might be missed. This is distinct from R35 (architecture map) and R37 (no stale references) — it is about surfacing the cross-cutting contracts explicitly.
