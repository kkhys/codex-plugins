# codex-plugins

> A personal Codex plugin marketplace for custom development workflows and tooling

## Plugins

| Plugin | Description |
|---|---|
| `base` | Personal development workflow for Codex: skills, hooks, and MCP servers. Empty for now; skills are added one at a time |

## Installation

```shell
codex plugin marketplace add kkhys/codex-plugins
codex plugin add base@codex-plugins
```

Codex refreshes git marketplaces at launch and caches each plugin by version under `~/.codex/plugins/cache/codex-plugins/<plugin>/<version>/`, so bump `version` in `plugins/base/.codex-plugin/plugin.json` with every change.

## Development

```shell
python3 scripts/validate-manifests.py
find plugins -name '*.sh' -print0 | xargs -0 -r shellcheck
```

The same checks run in CI via `.github/workflows/validate.yml`.

See [AGENTS.md](./AGENTS.md) for the repository layout and conventions.

## License

This marketplace and its included plugins are intended for personal use.
