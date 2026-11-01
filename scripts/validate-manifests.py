#!/usr/bin/env python3
"""Check the manifests Codex reads from this repository.

Codex has no `plugin validate` command, so this catches what otherwise
surfaces only at install time: a plugin path that does not exist, a plugin
whose directory name differs from its manifest name (Codex identifies a
plugin by its directory), and a skills directory that is missing.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load_json(path: Path):
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        fail(f"{path.relative_to(ROOT)}: {e}")
        return None


def check_plugin(entry: dict) -> None:
    name = entry.get("name")
    if not name:
        fail("marketplace.json: plugin entry without a name")
        return
    if not entry.get("category"):
        fail(f"{name}: category is required")

    source = entry.get("source")
    if not isinstance(source, dict) or source.get("source") != "local":
        fail(f'{name}: source must be {{"source": "local", "path": "./..."}}')
        return
    rel_path = str(source.get("path", ""))
    if not rel_path.startswith("./"):
        fail(f"{name}: source path must start with ./ (got {rel_path!r})")
        return

    plugin_root = ROOT / rel_path
    if not plugin_root.is_dir():
        fail(f"{name}: {rel_path} does not exist")
        return
    if plugin_root.name != name:
        fail(f"{name}: directory is named {plugin_root.name!r}; Codex uses the directory name")

    manifest = load_json(plugin_root / ".codex-plugin" / "plugin.json")
    if manifest is None:
        return
    if manifest.get("name") != name:
        fail(f"{name}: plugin.json name is {manifest.get('name')!r}")
    if not manifest.get("version"):
        fail(f"{name}: plugin.json has no version")

    skills = manifest.get("skills", "./skills")
    for rel in [skills] if isinstance(skills, str) else skills:
        if not (plugin_root / rel).is_dir():
            fail(f"{name}: skills directory {rel} does not exist")


def main() -> int:
    data = load_json(MARKETPLACE)
    if data is not None:
        if not data.get("name"):
            fail("marketplace.json: name is required")
        plugins = data.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            fail("marketplace.json: plugins must be a non-empty list")
        else:
            for entry in plugins:
                check_plugin(entry)
            names = [entry.get("name") for entry in plugins]
            for dup in sorted({n for n in names if names.count(n) > 1}):
                fail(f"marketplace.json: plugin {dup!r} is listed more than once")

    for message in errors:
        print(f"error: {message}", file=sys.stderr)
    if errors:
        return 1
    print("manifests ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
