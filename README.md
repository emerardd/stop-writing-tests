# stop-writing-tests

![A three-line code change on one side, a mountain of generated test files on the other](assets/hero.webp)

**Your agent changed 3 lines. Why did it write 300 lines of tests?**

A small agent skill that makes every new test earn its place.

> **Every new test must buy new confidence.**

Keep the regression tests. Skip the ceremony. Reuse existing coverage, fill real
gaps, and stop when the change is verified.

## Why install it?

Coding agents often treat every changed file as a reason to add tests. A small
refactor can grow into duplicate cases, new fixtures, snapshots, and helper
layers that add maintenance cost without adding confidence.

`stop-writing-tests` inserts one decision before that expansion:

- reuse relevant coverage when it already proves the behavior;
- add one focused regression when a real gap exists;
- avoid invented edge cases, duplicate matrices, and unnecessary test tooling;
- still run the checks needed to verify the change.

It is intentionally small and works alongside the repository's existing test
rules, including required checks and TDD workflows.

## Install

```sh
npx skills add emerardd/stop-writing-tests
```

Requires Node.js/npm. Follow the prompts to choose your agent and installation
scope. To try a downloaded or cloned copy locally, run
`npx skills add . --skill stop-writing-tests` from this repository's root.

Then use it in Codex:

```text
Use $stop-writing-tests while fixing the cache expiration bug.
```

Or in Claude Code:

```text
/stop-writing-tests Fix the cache expiration bug.
```

<details>
<summary>Installation options and troubleshooting</summary>

```sh
# Codex
npx skills add emerardd/stop-writing-tests --agent codex --global

# Claude Code
npx skills add emerardd/stop-writing-tests --agent claude-code --global
```

`--global` installs for your user account; the CLI defaults to project scope.
See the [Skills CLI documentation](https://github.com/vercel-labs/skills) for
installation options. The same options work with `.` as a local source.

Without Node.js/npm, download or clone the repository and copy
`skills/stop-writing-tests` to `~/.agents/skills/` for Codex or
`~/.claude/skills/` for Claude Code. For project-only installation, use the
corresponding directory inside the project.

Automatic activation depends on the host agent and its other instructions.
Invoke the skill explicitly when you need predictable use. If a newly installed
skill is not listed, start a fresh agent session. User requests and repository
testing requirements always take precedence.

</details>

## What changes after installation?

**Task:** Rename an internal configuration attribute. Keep the public config
format and behavior unchanged; existing tests already exercise the affected path.

| Typical agent behavior | With `stop-writing-tests` |
| --- | --- |
| Add near-duplicate unit tests | Reuse the test that already exercises the path |
| Expand fixtures and compatibility cases | Check whether any observable contract changed |
| Introduce a new integration harness | Run the repository's existing relevant checks |
| Leave more test code to maintain | Stop when the requested change is verified |

*Illustrative scenario, not a measured benchmark result.*

**A real bug with missing coverage gets a different answer:**

```text
Task: Fix the cache returning a value at its expiration time.

Agent:
  Reproduced the expiration-boundary failure.
  Added one focused regression: existing tests only cover unexpired reads.
  Fixed the comparison.
  Verified the regression and the relevant suite.
```

The goal is less test bloat with necessary protection intact. This skill never
authorizes deleting tests, weakening assertions, or skipping required checks.

## The decision

Before expanding the suite, identify:

1. **Failure:** What concrete problem would the addition detect?
2. **Gap:** What evidence is missing from relevant existing coverage?
3. **Authority:** Where is the expected behavior defined?
4. **Size:** What is the smallest worthwhile addition?

No grounded gap? Reuse the checks and stop. A real gap? Cover it.

This includes extra parameters, snapshots, fixtures, and helpers inside existing
files. It also leaves room for useful overlap: a fast unit regression and an
integration check can provide different evidence about the same bug.

Read the entire [skill](skills/stop-writing-tests/SKILL.md). It is the product.

## Works with your workflow

This skill does not replace a testing strategy or impose a framework. It makes
one small, upfront decision during ordinary coding tasks: whether expanding test
assets would add evidence that the repository does not already have.

It can fit a TDD workflow: reuse a failing regression when one exists, write a
focused one when missing, and follow the project's required process. It never
authorizes deleting tests, weakening assertions, or skipping mandatory checks.

## Evidence status

The decision rules are published and inspectable, but behavioral effectiveness
has not yet been benchmarked against untreated agents and a short-instruction
baseline. Until those results are available, treat this as a transparent,
editable default rather than a measured performance claim. See the
[research notes](RESEARCH.md) for design sources, related projects, and
evaluation boundaries.

## Contributing

A useful contribution is a small reproducible case where the skill adds needless
tests, misses necessary protection, invents a requirement, or slows work down.
Include the task, relevant existing coverage, agent/model version, transcript,
and diff. Remove secrets and private code. Prefer a demonstrated failure over
another universal rule.

## License

[MIT](LICENSE).
