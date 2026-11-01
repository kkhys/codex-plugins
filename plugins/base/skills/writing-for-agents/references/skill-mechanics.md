# Skill mechanics

The skill-specific branch of `writing-for-agents`: what changes when the
document is a skill. Everything else about writing it is the universal
reference in `SKILL.md`; frontmatter keys and size limits are in the
repository's `AGENTS.md`.

## What Codex does with a skill

Codex lists every discoverable skill to the model as `name: description
(file: path)` — a plugin skill carries the plugin name as prefix — and
reaches one implicitly when its description matches the turn; the user
reaches one explicitly by typing `$name` (`$plugin:name` for a plugin
skill). On either route the whole `SKILL.md` body is injected as written:
nothing is substituted into it, the request itself is the argument, and
relative paths resolve against the directory of `SKILL.md`, so a disclosed
reference is addressed as `references/x.md` after one line saying paths are
relative to the skill's directory. There is no fork, no per-skill tool list
and no per-skill hook: a clean context is a subagent the body asks for, and
a guardrail is a sentence in the body.

Of the frontmatter Codex reads `name`, `description`, and
`metadata.short-description`; `agents/openai.yaml` beside it carries the UI
metadata and the invocation policy.

## Invocation

Two choices, trading the two loads:

- An implicitly invocable skill — the default — keeps its description in the
  list, so the agent can fire it on its own, and other skills can reach it by
  naming `$name` in their prose. The user can still type its name: implicit
  invocation always includes explicit reach. The description is the skill's
  top-level context pointer, forced to stay loaded at all times — permanent
  context load in exchange for discoverability. A skill whose content is all
  reference is also the home for reference that several skills share: they
  reach it by naming it. Mechanics: no `policy` block in
  `agents/openai.yaml`, and a model-facing `description` carrying the trigger
  branches (the pointer rules in `SKILL.md` apply in full).
- An explicit-only skill leaves the list: only the human typing `$name`
  reaches it, and another skill's `$name` has nothing to resolve against.
  Zero context load, but it spends cognitive load — you are the index that
  must remember it exists. Mechanics: `policy.allow_implicit_invocation:
  false` in `agents/openai.yaml`; the `description` becomes human-facing — a
  one-line summary, trigger branches stripped.

Pick implicit invocation only when the agent must reach the skill on its own,
or another skill must. If it only ever fires by hand, make it explicit-only
and pay no context load.

Shared reference that two explicit-only skills both need can live in neither
— out of the list, neither can fire the other. Push it to a plain file
outside the skill system: external reference any skill can point at by path.

## Splitting by invocation

Split off an implicitly invocable skill when you have a distinct leading word
that should trigger it on its own — a trigger word you actually use in your
prompts — or another skill must reach it. You pay context load for the new
always-loaded description, so that independent reach has to be worth it.

## Router skills

When explicit-only skills multiply past what you can remember, that piled-up
cognitive load is cured by a router skill: one explicit-only skill that names
the others and when to reach for each, so the human has one skill to
remember instead of many. It can only hint, never fire them: explicit-only
skills are out of the list, so nothing but the human's `$name` reaches them.
