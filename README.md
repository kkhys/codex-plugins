# codex-plugins

> A personal Codex plugin marketplace for custom development workflows and tooling

## Plugins

| Plugin | Description |
|---|---|
| `base` | Git and PR workflow: `formatting-commit`, `splitting-commit`, `creating-branch-name`, `publishing-pr`, `creating-pr`, `creating-stacked-pr`, `resolving-merge-conflicts`, `cleaning-workspace`, `illustrating-pr`, `recording-pr-qa`. Review: `reviewing-pr`, `posting-pr-review`, `reading-unresolved-pr-comments`, `fixing-review-comments`, `resolving-pr-comments`, `babysitting-pr`, `diagnosing-ci-failure`, `merging-renovate-prs`. Working aids: `writing-for-agents`, `diagnosing-bugs`, `digging`, `creating-handoff`, `drafting-message`, `eli15`, `explaining-like-doraemon`. Explicit-only (`$base:<name>`): `publishing-pr`, `illustrating-pr`, `recording-pr-qa`, `cleaning-workspace`, `diagnosing-bugs`, `digging`, `creating-handoff`, `eli15`, `explaining-like-doraemon` |

## Installation

```shell
codex plugin marketplace add kkhys/codex-plugins
codex plugin add base@codex-plugins
```

Skills are invoked as `$base:<name>`, for example `$base:creating-pr`; Codex also picks the implicit ones up from their descriptions.

The plugin also ships the [serena](https://github.com/oraios/serena) MCP server (symbol-level navigation and editing through a language server, started with `uvx` and `--context=codex`). It pays off in typed codebases and costs startup time everywhere else, so turn it off per repository where it is not needed, in that repository's `.codex/config.toml`:

```toml
[plugins."base@codex-plugins".mcp_servers.serena]
enabled = false
```

Codex refreshes git marketplaces at launch and caches each plugin by version under `~/.codex/plugins/cache/codex-plugins/<plugin>/<version>/`, so bump the patch number of `version` in `plugins/base/.codex-plugin/plugin.json` with every change (`0.2.0` → `0.2.1`); the major and minor numbers do not move.

## Development

```shell
python3 scripts/validate-manifests.py
find plugins -name '*.sh' -print0 | xargs -0 -r shellcheck

bash plugins/base/skills/reading-unresolved-pr-comments/scripts/test-read-unresolved-pr-comments.sh
bash plugins/base/skills/fixing-review-comments/scripts/test-reply-to-review-threads.sh
bash plugins/base/skills/babysitting-pr/scripts/test-pr-watch.sh
bash plugins/base/skills/recording-pr-qa/scripts/test-qa-overlay.sh
```

The same checks run in CI via `.github/workflows/validate.yml`.

Some `base` skills are adapted from [openai/codex](https://github.com/openai/codex) (Apache-2.0), [mattpocock/skills](https://github.com/mattpocock/skills) (MIT), [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community) (Apache-2.0), and [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) (MIT) — see [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md).

See [AGENTS.md](./AGENTS.md) for the repository layout and conventions.

## License

This marketplace and its included plugins are intended for personal use.
