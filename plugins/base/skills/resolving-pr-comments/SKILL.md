---
name: resolving-pr-comments
description: Resolve review threads on the current PR through scripts/resolve-pr-comments.sh — every unresolved thread after the user confirms, or an explicit list of thread IDs. Use when asked to resolve, close, or mark review threads as done.
---

# Resolve PR Comments

Paths below are relative to this skill's directory.

## Before Running

Resolving a thread tells the reviewer their point was handled; resolving one that was not forces them to reopen it. Show how many threads will be resolved and wait for the user's go-ahead. Prefer the explicit form whenever the handled threads are known: a bulk resolve also closes threads that arrived while you were working, or ones deliberately left open pending a decision.

## Run

Specific threads — the IDs from `$reading-unresolved-pr-comments`; works from anywhere, since thread IDs are globally unique:

```bash
bash scripts/resolve-pr-comments.sh PRRT_kwDOAbc123 PRRT_kwDOAbc456
```

Every unresolved thread on the current branch's PR (the current directory must be a git repo whose branch has an open PR):

```bash
bash scripts/resolve-pr-comments.sh
```

## After Running

Report the script's summary. Surface the error details of any thread that failed to resolve, so the user can decide whether to retry or investigate.
