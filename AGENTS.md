# AGENTS.md

Personal Codex plugin marketplace. Codex is the only consumer: nothing here is written for Claude Code or any other agent.

## Layout

```
.agents/plugins/marketplace.json   # Marketplace registry; `name` is the install suffix (base@codex-plugins)
plugins/base/                      # The one plugin
  .codex-plugin/plugin.json        # Manifest; `version` drives cache refresh
  skills/<name>/SKILL.md           # Skills, invoked as $base:<name>
  skills/<name>/agents/openai.yaml # UI metadata and invocation policy
  skills/<name>/scripts/           # Helpers used by that one skill, plus its test-*.sh
  scripts/lib/                     # Helpers shared by skill scripts (bash sourced, jq via -L, GraphQL via cat)
  hooks/hooks.json                 # Event hooks (default path, declare in the manifest only to move it)
  .mcp.json                        # MCP servers (declare as `mcpServers` in the manifest)
scripts/validate-manifests.py      # Manifest and SKILL.md checks; Codex has no `plugin validate`
THIRD_PARTY_NOTICES.md             # Source, license, and derived paths of adapted skills
```

## What the files do not say

- Codex identifies a plugin by its directory name. `plugins/<dir>`, `name` in `plugin.json`, and `name` in `marketplace.json` stay identical; renaming the marketplace breaks every `base@codex-plugins` install
- Codex caches a plugin under `~/.codex/plugins/cache/codex-plugins/<plugin>/<version>/`, so every change to a plugin bumps the patch number of `version` in its `plugin.json` (`0.2.0` → `0.2.1`), never the major or minor — the number only has to differ, the same way as in `kkhys/claude-code-marketplace`
- Codex shows the model each skill as `base:<name>: description (file: <root>/<skill>/SKILL.md)` — plugin skills carry the plugin name as prefix in the list — with the root resolved to an absolute path, so a skill body refers to its own files with plain relative paths (`scripts/post-pr-review.sh`) after one line saying paths are relative to the skill's directory. The user's explicit mention is `$base:<name>` (the `$` picker inserts that form); cross-references inside a skill stay `$<name>`, which Codex resolves as long as the bare name is unique, and which keeps the skills working if they are ever installed outside the plugin. Scripts are run through their interpreter (`bash scripts/x.sh`) because the executable bit is not guaranteed to survive installation. Nothing is substituted in a body: no `$ARGUMENTS`, no dynamic command output. The user's message is the argument ("the PR named in the request, otherwise the current branch's PR")
- Of a skill's frontmatter Codex reads only `name`, `description`, and `metadata.short-description`. `description` is one line, under 1024 characters, without angle brackets; it states the capability, when it applies, and one boundary when a neighbouring skill would otherwise be picked. Keep it discriminating: no trigger-phrase lists
- A skill refers to another skill as `$name`; keep the chain in one direction. `publishing-pr` runs `creating-branch-name` → `splitting-commit` → `creating-pr`; `splitting-commit`, `fixing-review-comments`, `diagnosing-ci-failure`, and `babysitting-pr` commit through `formatting-commit`; `fixing-review-comments` starts with `reading-unresolved-pr-comments` and hands resolution to `resolving-pr-comments` only on request — `babysitting-pr` is the one caller that resolves the threads it addressed without asking; `reviewing-pr` runs its own `references/review-pass.md` per lens (in subagents when available) and posts through `posting-pr-review` only on request; `diagnosing-ci-failure` and `merging-renovate-prs` reuse `babysitting-pr`'s `scripts/pr-watch.sh` and `references/ci-heuristics.md` through `../babysitting-pr/` — keep those paths stable; `creating-stacked-pr` owns the stack-or-not verdict and sends command mechanics to the external `$gh-stack` skill (installed in `~/.agents/skills` by the dotfiles) and conflicts to `resolving-merge-conflicts`; `merging-renovate-prs` merges only in repositories owned by `kkhys` and confirms each merge with the user — a sandbox escalation is answered by the auto-review model, not the user, so it never counts as that confirmation
- `agents/openai.yaml` carries `interface.display_name`, `short_description` (25–64 chars), and a `default_prompt` that names `$skill`. `policy.allow_implicit_invocation: false` only for a user-timed workflow (`publishing-pr`); a skill with side effects stays discoverable and asks before the mutation instead
- Every comment the scripts post to GitHub starts with `[from Codex]`, so reviewers can tell an agent's comment from the user's own. `post-pr-review.sh` and `reply-to-review-threads.sh` prepend it idempotently (`scripts/lib/attribution.jq`) — write bodies without it; add it by hand on a plain `gh pr comment`
- Skill scripts resolve the shared lib relative to their own path (`"${SCRIPT_DIR}/../../../scripts/lib"`); the layout under the plugin cache is the same as in this repo, so the path holds after install
- Hooks are trusted per handler by a hash of its content, and plugin hooks are never trusted automatically: after changing a handler, re-trust it with `/hooks` in Codex. Events: `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, `Stop`, `Interrupt`
- `.mcp.json` ships only servers every Codex session may want; today that is `serena`, started through `uvx` from its git repository with `--context=codex` (Serena then hides the file, search, and shell tools Codex already has) and `--project-from-cwd`. A repository that does not need it sets `[plugins."base@codex-plugins".mcp_servers.serena] enabled = false` in its `.codex/config.toml`; the same table takes `enabled_tools` / `disabled_tools`. Documentation lookup and browser automation belong to the projects that use them, not here
- Skills ported from another project record the source, its license, and the derived paths in `THIRD_PARTY_NOTICES.md`

## Checks

Before committing, `python3 scripts/validate-manifests.py` passes, `find plugins -name '*.sh' -print0 | xargs -0 -r shellcheck` is silent, and every `test-*.sh` under `plugins/*/skills/*/scripts/` and `plugins/*/scripts/` passes. CI runs all three on pull requests and pushes to `main`; new test scripts need no CI change.

Bash scripts start with `#!/usr/bin/env bash` and `set -euo pipefail` (sourced libs set no options); Python scripts are stdlib only.

## Git

- Commits follow Conventional Commits with the plugin name as scope (`feat(base): …`); root changes omit the scope
- Pull requests are drafts titled `[main] <type>: <description>` and assigned to `kkhys`
