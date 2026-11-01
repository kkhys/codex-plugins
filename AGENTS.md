# AGENTS.md

Personal Codex plugin marketplace. Codex is the only consumer: nothing here is written for Claude Code or any other agent.

## Layout

```
.agents/plugins/marketplace.json   # Marketplace registry; `name` is the install suffix (base@codex-plugins)
plugins/base/                      # The one plugin
  .codex-plugin/plugin.json        # Manifest; `version` drives cache refresh
  skills/<name>/SKILL.md           # Skills, invoked as $name
  hooks/hooks.json                 # Event hooks (default path, declare in the manifest only to move it)
  .mcp.json                        # MCP servers (declare as `mcpServers` in the manifest)
scripts/validate-manifests.py      # Manifest checks; Codex has no `plugin validate`
```

## What the files do not say

- Codex identifies a plugin by its directory name. `plugins/<dir>`, `name` in `plugin.json`, and `name` in `marketplace.json` stay identical; renaming the marketplace breaks every `base@codex-plugins` install
- Codex caches a plugin under `~/.codex/plugins/cache/codex-plugins/<plugin>/<version>/`, so every change to a plugin bumps `version` in its `plugin.json`
- Of a skill's frontmatter Codex reads only `name`, `description`, and `metadata.short-description`; everything else is ignored, so the trigger phrasing goes in `description`. Per-skill interface and invocation policy live in `agents/openai.yaml` next to `SKILL.md`
- Hooks are trusted per handler by a hash of its content, and plugin hooks are never trusted automatically: after changing a handler, re-trust it with `/hooks` in Codex. Events: `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, `Stop`, `Interrupt`
- Skills ported from another project record the source, its license, and the derived paths in `THIRD_PARTY_NOTICES.md`

## Checks

Before committing, `python3 scripts/validate-manifests.py` passes and `find plugins -name '*.sh' -print0 | xargs -0 -r shellcheck` is silent. CI runs both on pull requests and pushes to `main`.

Bash scripts start with `#!/usr/bin/env bash` and `set -euo pipefail`; Python scripts are stdlib only.

## Git

- Commits follow Conventional Commits with the plugin name as scope (`feat(base): …`); root changes omit the scope
- Pull requests are drafts titled `[main] <type>: <description>` and assigned to `kkhys`
