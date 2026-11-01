---
name: creating-pr
description: 'Open a GitHub pull request with this user''s conventions — title "[base-branch] type: description", always --draft, always --assignee kkhys, a flat bullet body in the repository''s language. Use for any request to create or open a PR.'
---

# Creating PR

Start from `git branch --show-current`, `git status --short`, and `git log --oneline -15`. Uncommitted changes are not part of a PR: commit them first (`$formatting-commit`, or `$splitting-commit` when they mix concerns) or ask.

## Base Branch

In this order:

1. The branch the user named in the request (e.g. "develop にマージ")
2. The branch the current branch was created from
3. `main`

Pass it as `--base <branch>`; it also goes into the title brackets.

## Title

```
[base-branch] type: description
```

Base branch in brackets, then a Conventional Commits type and a lowercase English description — English whatever language the body uses, so a PR list scans by target and kind.

- `[main] feat: add user authentication system`
- `[develop] fix: resolve null pointer in login handler`
- `[main] refactor: extract validation logic`

When the changes span types, pick by primary purpose: feat > fix > perf > refactor > test > docs > style > ci > build > chore. A feature branch with bug fixes and tests is still `feat`.

## Body

Check for a PR template first (`.github/pull_request_template.md` or the other standard locations). With one, use it as the structure and fill its sections from the actual changes; with several, take the default `pull_request_template.md`, otherwise the one whose name best matches the change, and say which was used.

Language follows the repository: the template's language when there is one, otherwise the language of recent merged PRs (`gh pr list --state merged --limit 5 --json body --jq '.[].body'`); a repository with no history gets English.

Without a template, write a flat bullet list: imperative mood ("Add", "Fix", "Remove"), one concrete change per bullet, 3–5 bullets for the meaningful changes, no headings or sub-bullets, no "Summary" / "Test plan" sections.

Good:

```
- Switch image discovery from frontmatter field to directory-based auto-detection
- Consolidate getImage/getImages into getImagesForMemo
- Remove images field from content schema
```

## Create

Push the branch if it has no upstream, then `gh pr create` with:

- `--draft` — every PR starts as a draft so the author can self-review before requesting reviews
- `--assignee kkhys`
- `--base`, `--title`, `--body` as decided above

End with the PR URL `gh pr create` prints.
