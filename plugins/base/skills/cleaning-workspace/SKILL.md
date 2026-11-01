---
name: cleaning-workspace
description: Delete every local branch of the current repository except the protected ones — trunk branches, anything checked out in a worktree, names passed with --keep — after showing the list once and flagging work that exists nowhere else. Explicit workflow, invoked as $cleaning-workspace; never touches a worktree or a remote branch.
---

# Cleaning the Workspace

Reset the checkout to trunk only: no extra branches — merged ones, abandoned experiments, and stacks whose PRs were squash-merged. Worktrees are Orca's to create and remove, so this skill never touches one or the branch it has checked out.

Run first: `git branch --show-current`, and `git branch --format='%(refname:short)%09%(worktreepath)'` for every branch with the worktree that has it checked out.

## Process

1. Protected: `main`, `master`, `develop`, `staging`, `production`, every branch checked out in a worktree (the current one included), and every name the request passes after `--keep`.
2. List what will go — every other branch — and flag the ones that hold work nowhere else: commits missing from the branch's upstream, or no upstream at all (`git log --oneline <branch>@{upstream}..<branch>`). Ask once; `-D` destroys that work.
3. On yes: `git branch -D <branch> ...`
4. Report what was removed and what was kept, one line each.
