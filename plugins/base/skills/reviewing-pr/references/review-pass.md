# Review pass

A read-only, defect-first pass over one pull request through one lens. Do not modify files, create commits, push, post comments, or delegate further. Return every finding the author would likely fix.

## Inputs

- The repository checkout and the PR number
- The base and head refs
- One lens from the list below (all three when none is given)

## Read the change

1. Read the repository's `AGENTS.md` instructions.
2. Compare what would actually merge: `git merge-base <base> <head>`, then `git diff <merge-base> <head>` (`gh pr diff <number>` is the same diff when the branch is up to date with its base).
3. Read enough surrounding code to understand each changed path. Continue through the whole diff after the first issue.
4. Confirm each finding against the tests and the call sites before keeping it.

## Lenses

- `regressions`: behaviour the change breaks — wrong output, crash, data loss, security, performance — including callers the diff does not touch when a signature, return value, or behaviour changed
- `silent-failures`: errors swallowed or downgraded — empty or logging-only catch blocks, fallbacks that hide bad state, missing propagation at trust boundaries, success reported on a partial result
- `test-coverage`: changed behaviour with no test that would fail without the change, tests that assert the wrong thing, and the edge cases the diff introduces but never exercises

## Keep a finding only when all of these hold

- It affects correctness, security, performance, or maintainability in a meaningful way
- It is discrete and actionable
- It was introduced by the reviewed change
- The affected scenario or call path can be demonstrated from the code
- The author would probably fix it if they knew about it

Speculative concerns, pre-existing problems, intentional behaviour changes, and style nits that do not obscure the code are not findings.

## Output

Findings first, ordered by severity, one entry per issue:

`[P1] Imperative finding title — path/to/file:line`

followed by one short paragraph: the affected scenario and why the behaviour is wrong. Keep the cited range as small as possible and inside the reviewed diff.

- `P0`: release blocker or critical failure
- `P1`: urgent defect to fix next
- `P2`: ordinary defect to fix
- `P3`: low-impact issue still worth fixing

With no qualifying finding, say `No findings.` — never invent one. Close with a brief overall assessment and any material test gap or residual risk.
