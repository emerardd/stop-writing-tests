# Design and research notes

Sources were last checked on 2026-09-17. This document was revised on
2026-09-21. It records the design rationale, related work, and evaluation path
behind `stop-writing-tests`. The skill text and examples were written for this
project; no upstream skill body or code is vendored.

## Why this skill exists

Coding agents can turn a small implementation change into a much larger test
diff: duplicate cases, expanded parameter matrices, new snapshots, fixtures,
helpers, or even a new harness. That extra code is useful only when it adds
evidence the repository did not already have.

`stop-writing-tests` makes that decision explicit before test assets grow:

- reuse relevant coverage when it already proves the affected behavior;
- add the smallest focused regression when a real evidence gap exists;
- verify the change with the repository's existing tools either way.

The result is a small, installable default for keeping agent-written test changes
proportionate to the behavior and risk of the task.

## Focus and compatibility

The skill applies during ordinary coding work—bug fixes, refactors, renames,
configuration changes, and new behavior—before an agent decides to add or expand
tests. Its decision also covers parameter rows, snapshots, fixtures, helpers,
mocks, and test dependencies, not only new test files.

It does not prescribe a framework or testing pyramid. Existing protection,
explicit user requests, repository requirements, and mandatory checks remain in
force. It also fits TDD: reuse a failing regression when one exists, or add a
focused regression when the required behavior is not yet covered.

## Distribution and activation

- The [Agent Skills specification](https://agentskills.io/specification) defines
  a skill as a folder containing `SKILL.md` with `name` and `description` fields.
  This package intentionally ships one instruction file.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) documents
  Codex discovery from personal and project skill directories, including
  `~/.agents/skills`.
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
  documents personal and project skill directories and `/skill-name` invocation.
- The [Vercel Labs Skills CLI](https://github.com/vercel-labs/skills) installs
  skills from GitHub repositories or local directories at project or global
  scope. The root README uses it as the primary installation path.

Remote installation targets `emerardd/stop-writing-tests`. A cloned copy can be
discovered with `npx skills add . --skill stop-writing-tests`. Node.js/npm is
needed by the installer, not by the installed Markdown skill. Explicit invocation
is the most predictable way to confirm that the host loaded it for a task.

## Relationship to other approaches

`stop-writing-tests` complements broader testing guidance and test-first
workflows while packaging a smaller decision point.

- [amElnagdy/guard-skills: test-guard](https://github.com/amElnagdy/guard-skills/blob/master/skills/test-guard/SKILL.md)
  reviews whether generated tests are valuable and can also be used upfront.
  `stop-writing-tests` concentrates on whether test assets should grow at all
  during the current coding task.
- [nickperkins/testing-skill](https://github.com/nickperkins/testing-skill)
  covers testing layers, redundant coverage, brittle assertions, and E2E scope.
  `stop-writing-tests` is framework-independent and includes the valid outcome
  of reusing verification without adding a persistent test asset.
- [obra/superpowers: TDD](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md)
  organizes implementation around the red/green/refactor cycle.
  `stop-writing-tests` can operate inside that workflow by keeping the regression
  and its surrounding test changes focused on the missing evidence.

The standalone value is scope: one memorable rule—every new test must buy new
confidence—applied before a coding agent expands the suite.

## Evaluation path

A comparative evaluation should include three conditions:

1. the task and repository instructions alone;
2. the same task plus a one-sentence restraint instruction;
3. the same task with the complete `stop-writing-tests` skill.

Cases should include both changes already covered by relevant tests and real bugs
or public contracts that need new protection. Useful outcomes include task
correctness, necessary gaps found, redundant assets avoided, invented contracts
avoided, verification executed, and maintenance surface added.

The intended result is fewer low-value test additions without fewer necessary
regressions or weaker verification. Host activation should be checked separately
so installation problems are not confused with instruction quality.

Published evaluations should include reproducible tasks, agent and model versions,
transcripts, diffs, and independently checkable outcomes. That keeps installation,
host activation, and behavioral value separately auditable.
