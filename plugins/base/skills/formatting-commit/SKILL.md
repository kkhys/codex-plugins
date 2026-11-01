---
name: formatting-commit
description: Write git commit messages in Conventional Commits form with this user's scope and amend rules, and decide between a new commit and an amend. Use whenever changes are committed, including commits made inside another workflow.
---

# Formatting Commit

Start from `git status --short` and `git log --oneline -10`; `git log --oneline origin/main..HEAD` shows the branch-only commits when the branch has a PR.

## New commit or amend

New commit by default. Amend only when all of these hold: the previous
commit is not pushed, the change is a fixup of that commit (typo, forgotten
file), and a separate commit would be noise.

Under review the answer is always a new commit — one per fix round, scoped
to what that round changed — and a plain push. Amending a pushed commit
force-pushes, which detaches existing review comments from their lines and
erases the per-round diff the reviewer uses to check that their feedback
landed.

Reorganising several existing commits is `$splitting-commit`'s job, not a
manual rebase here.

## Message

```
<type>(<scope>): <description>
```

Type by dominant intent, one of `feat` `fix` `refactor` `perf` `test`
`docs` `style` `build` `ci` `chore`. A feature with its tests is `feat`; a
bug fix with incidental refactoring is `fix`.

Scope is the area of the codebase, and the recent log shows the repository's
own convention (a plugin marketplace uses the plugin name, dotfiles use the
tool name). Omit it only for cross-cutting root changes.

Subject: imperative, lowercase, no trailing period, under 50 characters. A
body, when the change is non-trivial, says why — the subject already says
what. `!` after the type marks a breaking change.

## Process

1. Stage specific files — be deliberate about what goes in
2. Commit, then verify with `git log -1 --stat`
