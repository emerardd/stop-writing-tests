---
name: stop-writing-tests
description: Prevent unnecessary test growth during coding tasks. Use when fixing bugs, refactoring, renaming, changing configuration, or adding behavior, before deciding whether to add or expand tests. Identify worthwhile coverage gaps, reuse existing verification, and keep necessary regression coverage.
license: MIT
---

# stop-writing-tests

**Every new test must buy new confidence.**

Default to reusing relevant coverage. A changed file is not a reason to add tests.
Apply this judgment to new test functions, parameter rows, snapshots, fixtures,
helpers, and dependencies, including additions inside existing files.

## Before expanding tests

Read the task, applicable repository instructions, and the relevant existing tests.
Look for the smallest useful evidence gap:

- What concrete failure or important boundary would this addition detect?
- What relevant coverage exists, and what evidence would the addition contribute?
- Where does the expected behavior come from: the request, a documented contract,
  established behavior, or a reproduced bug?
- Can an existing test, one extra assertion, or a smaller regression case cover it?

Make a proportionate inspection, not an exhaustive suite audit. If coverage cannot
be inspected or run, report that uncertainty; do not claim it exists or passes.

Add the smallest worthwhile test when there is a grounded gap. A reproduced bug,
new public behavior, changed contract, or security invariant can justify one.
For a bug, reproduce the original failure with existing coverage first; add a
focused regression if missing, and verify it fails for the bug and passes the fix
when feasible. Do not expand a matrix just because more cases are imaginable.

Overlap alone does not make a test redundant: a different integration boundary,
or a substantially faster, more reliable regression signal, can justify it.
Explain that benefit instead of pretending every test must catch a unique bug.
Honor explicit user requests and applicable repository testing requirements;
this skill is not a reason to refuse required tests or mandatory checks.

If no worthwhile gap remains, do not expand the suite. Renames, code moves,
formatting, comments, internal branches, and coverage percentages are not reasons
by themselves. Judge actual behavior and risk: a public config rename can change
a contract even when the diff is tiny.

## Keep the evidence honest

- Do not invent expected behavior to fill a speculative edge case. Surface a
  consequential ambiguity and ask a focused question when needed; continue work
  that does not depend on that decision.
- Derive expectations independently from requirements, known examples, or an
  independent oracle. Copying production logic into an expected-value calculator
  can reproduce the same error. Prefer observable behavior over private call order.
- Reuse the repository's test tools. New frameworks, harnesses, mocks, snapshots,
  or helper layers need a concrete benefit proportionate to the task.
- Preserve existing protection. Do not delete or skip tests, weaken assertions,
  or lower coverage thresholds to achieve fewer tests or a passing result.
  Update an existing expectation only when an authorized behavior change requires
  it; preserve unrelated assertions and explain the contract change.

## Verify, then stop

Run the narrowest relevant existing checks, plus required repository checks.
Expand verification for material risk, failures, or further changes; stop once
the needed evidence is obtained. Documentation-only work may need a docs build
or link check rather than code tests. Adding no test does not mean no verification.

Keep the decision brief: one sentence identifying the added evidence or the
reused coverage is usually enough. Report what actually ran and any limitations.
Do not turn these questions into a mandatory report or approval ceremony.
