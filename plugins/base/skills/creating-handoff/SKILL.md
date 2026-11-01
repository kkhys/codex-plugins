---
name: creating-handoff
description: Compact the current conversation into a handoff document — a file under ~/.agents/handoffs/, or appended to a Notion page — so a fresh session can continue the work. A transit document, not a spec or a plan; it carries only what the next session needs to resume.
---

# Creating Handoff

Write a handoff document summarising the current conversation so a fresh
agent can continue the work. The reader has none of this context, so the file
must stand on its own — but it is a transit document, not a spec: enough to
resume, nothing that already lives elsewhere.

## Next session

The focus named in the request. If none is named, the next session continues
the current task. Otherwise tailor the whole document to that focus — what it
needs to know, in the order it needs it.

A Notion page URL in the request changes the destination: append the
document to the bottom of that page with the Notion MCP tools instead of
writing a file — that is how work crosses sessions in a shared workspace —
and skip the file unless the user asks for both. When no Notion tools are
configured, say so and write the file.

## Session context

Run these first; the output feeds the header and the Artifacts section:

```bash
date '+%Y%m%d-%H%M'
git rev-parse --show-toplevel 2>/dev/null || echo "not a git repo"
git branch --show-current 2>/dev/null
git log --oneline -5 2>/dev/null
gh pr view --json number,url,title 2>/dev/null || echo "no PR"
```

## Document structure

Write in English; quote the user's own requirements verbatim in their
original language.

```markdown
# Handoff: <title>

Written <YYYY-MM-DD HH:mm> from <repo>@<branch> — for: <next-session focus>

## State
<done / in progress / blocked — one line each>

## Decisions
<each with its reason; the rejected alternative in one clause>

## Open questions

## Artifacts
<one path or URL per line: plan file, spec, PR, commits (short sha),
branch, gist>

## Environment notes
<commands that worked, what failed and why, gotchas>

## Suggested skills
<`$plugin:skill` — when the next agent should invoke it>

## Next steps
<ordered>
```

Do not duplicate content already captured in other artifacts (specs, plans,
ADRs, issues, commits, diffs). Reference them by path or URL instead, and
verify each referenced path exists before citing it. Under Suggested skills,
name only skills present in this environment, as `$plugin:skill`.

## Content safety

A handoff travels — into another session, another machine, sometimes another
person's hands — so treat it as semi-public. Before writing, scan the draft
for credentials, tokens, API keys, internal hostnames, PII, `.env` values,
and database connection strings; replace each with `<REDACTED>`. If a
redacted value looks load-bearing for the next session, or you are unsure
whether something is sensitive, flag it and ask the user before writing.

## Writing the file

1. `mkdir -p ~/.agents/handoffs`
2. Name the file `<YYYYMMDD-HHmm>-<slug>.md`, using the timestamp above. The
   slug is 2–5 lowercase ASCII words joined by hyphens, taken from the
   next-session focus (or the session topic when the focus is blank). A
   Japanese topic becomes short English words, not romaji.
3. Write it in one go.

## Report

Reply in Japanese with the absolute path or the page URL, a one-line summary
of what the document covers, what was redacted (or 「秘匿情報なし」), and how
to resume:

```
新しいセッションで「~/.agents/handoffs/<file> を読んで続きをやって」（Notion なら「<page URL> の末尾を読んで続きをやって」）と伝えてください。
```
