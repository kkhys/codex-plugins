---
name: reading-unresolved-pr-comments
description: Fetch the current PR's unresolved review threads — thread IDs, outdated flags, line ranges, full comment history — through scripts/read-unresolved-pr-comments.sh and turn them into a fix plan. Use to see what reviewers asked for; the first step of fixing-review-comments. Reads only.
---

# Read Unresolved PR Comments

Paths below are relative to this skill's directory. The current branch must have an open PR.

## Fetch

```bash
scripts/read-unresolved-pr-comments.sh
```

Returns JSON with the PR metadata and every unresolved thread: `thread_id`, `path`, `line`, `start_line`, `is_outdated`, and the comments. Comments on a reviewer's unsubmitted PENDING review are already filtered out.

## Fix Plan

No unresolved threads: report that and stop.

For each thread, capture both the specific ask and the underlying intent — "rename this variable" often means "this name says X while the value is Y". Then:

1. Group comments on the same file or function — coordinated changes reduce conflicts
2. Order groups by dependency, foundational changes first
3. Per item: file path, line, the reviewer's concern (the why), the concrete action
4. Mark `is_outdated` threads — the code may already have changed, so verify the current state before planning a fix
5. Make each item independently actionable, since `$fixing-review-comments` may hand them to subagents in parallel

## Scope

Read and plan only: no code changes, no thread resolution, no push. The plan is the checkpoint the user or the calling skill reviews before any code is touched.
