---
name: splitting-commit
description: Split uncommitted changes that mix several concerns into a sequence of focused commits a reviewer can follow and git bisect can act on. Not for a single-concern change, which goes straight to formatting-commit.
---

# Splitting Commits

Split uncommitted changes into focused commits, each one logical concern, so the history tells a story a reviewer can follow and `git bisect` and `git revert` can act on cleanly.

## When to Split

A concern is a unit of intent: a bug fix, a feature, a refactoring, a dependency update. If the change fits one Conventional Commits subject without "and", it is one concern — commit it directly with `$formatting-commit`.

Don't over-split. Three related files changed for one feature = one commit. A rename touching 12 files = one commit. The question is always: would a reviewer want to see these together or separately?

## Workflow

### 1. Survey

`git status --short` and `git diff HEAD --stat` show what changed; read the full `git diff HEAD` before grouping. Understand what every change does and why before planning the split.

### 2. Plan

Identify distinct concerns and map files to each. Write the plan out before staging anything — this catches ordering mistakes early.

- Dependencies: utility and infrastructure changes come before features that use them; schema before code that reads it
- Reviewability: a reviewer reads commits in order, so earlier commits build context for later ones
- Revertability: if a single commit cannot be reverted without breaking the others, those changes belong together

When a file touches multiple concerns, put it in the dominant one. Clean file-level splits are more reliable than per-hunk staging and almost always sufficient.

### 3. Execute

For each group, in dependency order:

```bash
git add <file1> <file2> ...
git diff --cached --stat
git diff --cached
```

Then compose the message and commit with `$formatting-commit`, and move to the next group.

### 4. Verify

`git log --oneline origin/main..HEAD` should read as a coherent narrative. If something looks off, `git reset --soft HEAD~N` and re-split.

## Split Patterns

| Situation | Commits | Why |
|---|---|---|
| Feature + its tests | 1 | Tests validate the feature — the same concern |
| Feature + unrelated bug fix found along the way | 2 | Independent concerns with no dependency |
| Refactor + feature built on it | 2 (refactor first) | Separating makes the refactor reviewable on its own |
| Bug fix + feature that exposed the bug | 2 (fix first) | The fix is independently valuable and may be cherry-picked |
| Dependency update + code adapting to the new API | 1 | The old code breaks without the update |
| Config + code using the new config | 1 if tightly coupled, 2 if the config stands alone | Judgment call |
| Rename/move + logic changes | 2 (rename first) | Pure renames produce clean diffs; mixed-in logic hides them |

## Anti-patterns

- Splitting by file instead of by concern: incoherent commits with no clear intent
- Separating tests from the implementation they verify
- "Cleanup" commits for changes that only make sense with the feature they enable
- Over-splitting trivial changes: a typo fix + import cleanup = one `chore` commit
