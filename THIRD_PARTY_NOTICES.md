# Third-party notices

Skills in this marketplace that are ported or adapted from other projects, with
their licenses. Each entry lists the upstream source and the derived files here.

## openai/codex

- Source: https://github.com/openai/codex (tag `rust-v0.166.0`), the bundled system skill `review-agent` (`codex-rs` resources, installed as `$CODEX_HOME/skills/.system/review-agent/SKILL.md`)
- License: Apache-2.0 — Copyright 2025 OpenAI
- Derived file (modified from the original):
  - `plugins/base/skills/reviewing-pr/references/review-pass.md` — the read-only declaration, the merge-base comparison, the five conditions a finding must meet, and the `[P1] title — path:line` / P0–P3 / `No findings.` output form are from `review-agent/SKILL.md`; the lenses are this project's own

The Apache-2.0 boilerplate notice that upstream applies to its sources:

```
Copyright 2025 OpenAI

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## dietrichgebert/ponytail

- Source: https://github.com/dietrichgebert/ponytail (commit `96608e0`)
- License: MIT — Copyright (c) 2026 DietrichGebert
- Derived file (modified from the original):
  - `plugins/base/skills/reviewing-pr/SKILL.md` — the read-past-the-diff step, the assumed-load line, the concrete-case rule and the problem / fix / if-skipped shape of a finding are adapted from `skills/ponytail-review/SKILL.md`; the verdict block is this project's own

```
MIT License

Copyright (c) 2026 DietrichGebert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
