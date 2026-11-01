# codex-plugins

> A personal Codex plugin marketplace for custom development workflows and tooling

## Plugins

| Plugin | Description |
|---|---|
| `base` | Git workflow skills: `formatting-commit`, `splitting-commit`, `creating-branch-name`, `publishing-pr` (explicit only), `creating-pr`, `reviewing-pr`, `posting-pr-review`, `reading-unresolved-pr-comments`, `fixing-review-comments`, `resolving-pr-comments` |

## Installation

```shell
codex plugin marketplace add kkhys/codex-plugins
codex plugin add base@codex-plugins
```

Skills are invoked as `$base:<name>`, for example `$base:creating-pr`; Codex also picks the implicit ones up from their descriptions.

Codex refreshes git marketplaces at launch and caches each plugin by version under `~/.codex/plugins/cache/codex-plugins/<plugin>/<version>/`, so bump `version` in `plugins/base/.codex-plugin/plugin.json` with every change.

## Development

```shell
python3 scripts/validate-manifests.py
find plugins -name '*.sh' -print0 | xargs -0 -r shellcheck

bash plugins/base/skills/reading-unresolved-pr-comments/scripts/test-read-unresolved-pr-comments.sh
bash plugins/base/skills/fixing-review-comments/scripts/test-reply-to-review-threads.sh
```

The same checks run in CI via `.github/workflows/validate.yml`.

Some `base` skills are adapted from [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) (MIT) — see [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md).

See [AGENTS.md](./AGENTS.md) for the repository layout and conventions.

## License

This marketplace and its included plugins are intended for personal use.
