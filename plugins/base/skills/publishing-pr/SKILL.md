---
name: publishing-pr
description: Publish the current work end to end — branch, logical commits, draft pull request — by running creating-branch-name, splitting-commit, and creating-pr in sequence. Explicit workflow, invoked as $publishing-pr.
---

# Publish Workflow

`gh` and `git push`/`fetch` need the network: when sandboxed, run them with escalation.

Carry the working tree from uncommitted changes to an open draft PR.

If `git status --short` is empty and `git log --oneline @{upstream}..HEAD` shows nothing (or the branch has no upstream and no commits beyond `origin/main`), report that there is nothing to publish and stop.

Run these in order, finishing each before the next:

1. `$creating-branch-name` — skip when already on a feature branch
2. `$splitting-commit` — one commit per concern; a single-concern change is one commit via `$formatting-commit`
3. `$creating-pr` — push and open the draft PR

End with the PR URL.
