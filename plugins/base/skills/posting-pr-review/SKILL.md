---
name: posting-pr-review
description: Post review findings to a GitHub pull request as a PENDING review through scripts/post-pr-review.sh — severity-tagged, one or two lines each, substantive findings only, attributed to Codex. Use whenever review comments are to be posted or submitted to a PR; never call the review API directly.
---

# Post PR Review as PENDING

Paths below are relative to this skill's directory. `gh` and `git push`/`fetch` need the network: when sandboxed, run them with escalation.

The review is always created in PENDING state — never APPROVE or REQUEST_CHANGES — so the user can review and edit the comments on GitHub before the PR author is notified.

## Prerequisites

Review results from this session: the findings of `$reviewing-pr`, or findings the user supplied. Without them, ask:

> セッション内にレビュー結果が見つかりません。先にレビューを実行するか、レビュー内容を提供してください。

## What gets posted

Only findings that change behaviour, correctness, security, or performance for a user. Naming, style, comment wording, optional refactors, and praise stay out unless the user asks for exhaustive feedback — then `[nit]` and `[praise]` tags are available.

## Severity Tags

Every comment starts with a severity tag on its own line, then a body of one or two lines in a reviewer's plain Japanese — no preamble, no restating the diff.

| Tag | Meaning |
|---|---|
| `[critical]` | Bugs, security, data loss — must fix before merge |
| `[warning]` | Logic errors, performance, edge cases — should fix |
| `[question]` | Unclear intent — reply needed |
| `[suggestion]` | A concrete better approach, usually with a suggestion block |

```
[warning]
This catch block swallows the error silently. Consider logging or re-throwing.
```

## Attribution

The script prefixes the review summary and every comment with `[from Codex]`, producing `[from Codex] [warning]` on the first line. Write bodies without the marker. The PR author needs to tell agent-authored feedback from a human reviewer's, since the two carry different weight.

## Suggestion Blocks

When the fix is a concrete, small change, use a GitHub suggestion block; the author applies it with one click.

````
[warning]
`TECM-**` is shell glob notation, not a regex.

```suggestion
const match = branchName.match(/TECM-[0-9]+/);
```
````

- The suggestion block replaces exactly the line(s) the comment is attached to
- For multi-line suggestions, use `start_line` + `line` to define the range
- Only when the replacement is unambiguous — not for structural rewrites

## Workflow

### 1. Collect and Validate Findings

From each finding take the file path (relative to the repo root), the line number, the severity tag, and the body (with a suggestion block where applicable).

Verify that each line falls within `gh pr diff`. The GitHub API rejects comments on lines outside the diff, so this check is mandatory. A line outside the diff attaches to the nearest changed line in the same file, with the actual line number noted in the body; a file with no changes in the diff goes to step 3.

### 2. Post the PENDING Review

Write the payload JSON and pass it to the script:

```bash
bash scripts/post-pr-review.sh /path/to/payload.json
```

```json
{
  "body": "Review summary (optional)",
  "comments": [
    {
      "path": "src/example.ts",
      "line": 42,
      "body": "[warning]\nThis catch block swallows errors silently."
    },
    {
      "path": "src/utils.ts",
      "start_line": 10,
      "line": 15,
      "body": "[suggestion]\nExtract this into a helper.\n\n```suggestion\nconst result = extractHelper(input);\n```"
    }
  ]
}
```

- `path`: file path relative to the repo root (required)
- `line`: line number within the diff (required)
- `body`: comment starting with the severity tag (required)
- `side`: `RIGHT` (default, new code) or `LEFT` (deleted code)
- `start_line` / `start_side`: for multi-line comments

The script resolves the PR from the current branch and fails with a clear message when there is none.

### 3. Post General Comments

Findings on files outside the diff go in as general PR comments. Nothing prepends the marker here, so include it yourself:

```bash
gh pr comment --body "[from Codex] [severity]
Comment about non-diff code..."
```

### 4. Report

Severity counts and the PR URL, in Japanese:

> PENDING レビューを投稿しました。
>
> - [critical]: 1 件
> - [warning]: 3 件
> - [suggestion]: 2 件
>
> PR で確認して送信してください: https://github.com/owner/repo/pull/123
