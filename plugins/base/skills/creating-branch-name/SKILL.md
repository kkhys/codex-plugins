---
name: creating-branch-name
description: Create a git branch named type/description from the current changes. Use when asked for a branch, or when work sits on main or master and needs a branch before committing.
---

# Branch Naming

Derive the name from `git status --short`, `git diff HEAD --stat`, and `git log --oneline -5`; run `git diff` only when that is not enough.

## Convention

Format: `<type>/<description>`

Types, as full words: `feature/`, `fix/`, `refactor/`, `docs/`, `style/`
(visual or formatting), `chore/` (tooling, config, dependencies, CI).

Description: English, kebab-case, 2–4 words for the main intent. Start with
a verb when it reads naturally (`feature/add-login-authentication`,
`refactor/extract-shared-utils`); for `fix/` the problem itself is often
clearer (`fix/pagination-off-by-one`). Mixed changes are named for the
dominant intent.

## Process

1. Pick the type and description; when the intent is genuinely ambiguous,
   propose two or three candidates and let the user choose
2. `git checkout -b <name>`, then state the name and the reasoning in one line
