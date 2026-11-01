#!/usr/bin/env python3
"""Check the manifests and skills Codex reads from this repository.

Codex has no `plugin validate` command, so this catches what otherwise
surfaces only at install or load time: a plugin path that does not exist, a
plugin whose directory name differs from its manifest name (Codex identifies
a plugin by its directory), a missing skills directory, and SKILL.md
frontmatter Codex would reject or misread (the rules mirror the bundled
skill-creator's quick_validate.py, minus the PyYAML dependency: frontmatter
here is one `key: value` per line, plus an indented `metadata:` block).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

SKILL_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SKILL_NAME_MAX = 64
SKILL_DESCRIPTION_MAX = 1024

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path):
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        fail(f"{rel(path)}: {e}")
        return None


def parse_frontmatter(text: str, where: str):
    """Return the frontmatter as a dict, or None after recording the error."""
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        fail(f"{where}: no YAML frontmatter")
        return None
    data: dict = {}
    current = None
    for lineno, line in enumerate(match.group(1).splitlines(), start=2):
        if not line.strip():
            continue
        if line.startswith("  ") and current is not None and isinstance(data[current], dict):
            key, sep, value = line.strip().partition(":")
            if not sep:
                fail(f"{where}:{lineno}: expected `key: value`")
                return None
            data[current][key.strip()] = value.strip().strip("\"'")
            continue
        if line.startswith((" ", "\t")):
            fail(f"{where}:{lineno}: multi-line values are not supported; write the value on one line")
            return None
        key, sep, value = line.partition(":")
        if not sep:
            fail(f"{where}:{lineno}: expected `key: value`")
            return None
        key = key.strip()
        value = value.strip()
        if value in ("", "|", ">", "|-", ">-"):
            if value:
                fail(f"{where}:{lineno}: multi-line values are not supported; write the value on one line")
                return None
            data[key] = {}
            current = key
        else:
            data[key] = unquote(value, f"{where}:{lineno}")
            current = None
    return data


def unquote(value: str, where: str) -> str:
    """Strip YAML quotes; an unquoted value with `: ` or ` #` would not parse as one scalar."""
    if value[0] == "'" and value[-1] == "'" and len(value) > 1:
        return value[1:-1].replace("''", "'")
    if value[0] == '"' and value[-1] == '"' and len(value) > 1:
        return value[1:-1]
    if ": " in value or " #" in value:
        fail(f"{where}: quote the value; YAML splits an unquoted value at `: ` or ` #`")
    return value


def check_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    where = rel(skill_md)
    if not skill_md.is_file():
        fail(f"{rel(skill_dir)}: SKILL.md not found")
        return
    data = parse_frontmatter(skill_md.read_text(encoding="utf-8"), where)
    if data is None:
        return

    unexpected = sorted(set(data) - SKILL_FRONTMATTER_KEYS)
    if unexpected:
        fail(f"{where}: unexpected frontmatter key(s): {', '.join(unexpected)}")

    name = data.get("name")
    if not isinstance(name, str) or not name:
        fail(f"{where}: name is required")
    else:
        if name != skill_dir.name:
            fail(f"{where}: name is {name!r} but the directory is {skill_dir.name!r}")
        if not SKILL_NAME_RE.match(name):
            fail(f"{where}: name must be lowercase letters, digits, and single hyphens")
        if len(name) > SKILL_NAME_MAX:
            fail(f"{where}: name is longer than {SKILL_NAME_MAX} characters")

    description = data.get("description")
    if not isinstance(description, str) or not description:
        fail(f"{where}: description is required")
    else:
        if len(description) > SKILL_DESCRIPTION_MAX:
            fail(f"{where}: description is longer than {SKILL_DESCRIPTION_MAX} characters")
        if "<" in description or ">" in description:
            fail(f"{where}: description cannot contain angle brackets")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.is_file() and isinstance(name, str):
        yaml_text = openai_yaml.read_text(encoding="utf-8")
        if "default_prompt" in yaml_text and f"${name}" not in yaml_text:
            fail(f"{rel(openai_yaml)}: default_prompt must mention ${name}")


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
    for skills_rel in [skills] if isinstance(skills, str) else skills:
        skills_dir = plugin_root / skills_rel
        if not skills_dir.is_dir():
            fail(f"{name}: skills directory {skills_rel} does not exist")
            continue
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            check_skill(skill_dir)


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
