---
name: fixing-review-comments
description: Address the unresolved review comments on a pull request end to end — read the threads, check each against the code, implement what holds, verify, commit the round, reply in every thread with the commit link. Use when asked to fix, handle, or respond to PR review feedback.
---

# Fix Review Comments

Paths below are relative to this skill's directory.

## Target

The PR named in the request (URL or number), optionally narrowed to one thread (`#discussion_r<id>` — match it against the comment `url` fields in the fetched threads and handle only that one). Blank means the current branch's PR.

Run every step from a checkout of the PR's head branch — the scripts resolve the PR from the current branch. When this checkout is on another branch, neither switch it nor add a worktree (worktrees are opened in Orca): name the head branch, and the path from `git worktree list` if another worktree has it, and stop.

## Phase 1: Understand the Feedback

`$reading-unresolved-pr-comments` fetches every unresolved thread and returns a fix plan with the reviewer's underlying intent, outdated flags, and grouping.

Then check each item against the code before changing anything. A comment can be wrong, already addressed, or a judgment call:

- Wrong or already handled → no code change; the reply carries the evidence (the line that already does it, the reason the concern does not apply)
- A product or design decision → surface it with a suggested reply and wait

Only the remaining items go to Phase 2.

## Phase 2: Implement Fixes

Independent fixes (different files, no shared state) can go to subagents in parallel, each given the review comment, file path, line range, and the specific change; related fixes (same file, overlapping logic) run sequentially.

When a reviewer suggests an approach but leaves room for alternatives, make the call that best serves the codebase and note the reasoning — it goes into the thread reply.

## Phase 3: Verify and Commit

Run the project's tests and linter; fix what fails before going on. Commit every fix of this round as one new commit via `$formatting-commit` — never amend under review — and push with plain `git push`. One commit per round keeps the reviewer's per-round diff intact.

## Phase 4: Close the Loop

For each thread handled, reply with what was changed — specific enough that the reviewer can confirm without reading the diff — or, for a comment that needed no change, the evidence; plus the commit link when there is one:

```bash
COMMIT_URL="$(gh api "repos/$(gh repo view --json nameWithOwner -q '.nameWithOwner')/commits/$(git rev-parse HEAD)" --jq '.html_url')"
```

Post all replies at once:

```bash
bash scripts/reply-to-review-threads.sh /path/to/replies.json
```

```json
{
  "replies": [
    {
      "thread_id": "<thread ID from Phase 1>",
      "body": "<COMMIT_URL> で修正しました。[具体的な修正内容]"
    }
  ]
}
```

Replies are in Japanese, one specific sentence each.

### Attribution

The script prefixes every reply with `[from Codex]`, so write the body without it. Reviewers need to tell an agent's reply from the user's own — an unmarked reply reads as a personal commitment from the user. Put the same marker on anything posted with plain `gh pr comment`, where nothing adds it.

### Thread Resolution

Do not resolve threads: resolution is the reviewer's call. When the user explicitly asks for it, `$resolving-pr-comments` resolves the threads handled here by ID.
