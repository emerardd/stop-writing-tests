# stop-writing-tests

**Your agent changed 3 lines. Why did it write 300 lines of tests?**

A small agent skill that makes every new test earn its place.

> **Every new test must buy new confidence.**

Keep the regression tests. Skip the ceremony. Reuse existing coverage, fill real
gaps, and stop when the change is verified.

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
<summary>Choose an agent and install for all your projects</summary>

```sh
# Codex
npx skills add emerardd/stop-writing-tests --agent codex --global

# Claude Code
npx skills add emerardd/stop-writing-tests --agent claude-code --global
```

`--global` installs for your user account; the CLI defaults to project scope.
See the [Skills CLI documentation](https://github.com/vercel-labs/skills) for
installation options. The same options work with `.` as a local source.

</details>

<details>
<summary>Manual installation without Node.js/npm</summary>

Download this repository with GitHub's **Code → Download ZIP**, extract it, and
open a terminal in the extracted directory. Or use an existing local clone.
Copy the single skill folder to your agent's personal skills directory:

| Agent | Destination | Explicit invocation |
| --- | --- | --- |
| Codex | `~/.agents/skills/stop-writing-tests/` | `$stop-writing-tests` |
| Claude Code | `~/.claude/skills/stop-writing-tests/` | `/stop-writing-tests` |

**PowerShell — Codex:**

```powershell
$skillTarget = Join-Path $HOME '.agents/skills/stop-writing-tests'
if (Test-Path -LiteralPath $skillTarget) { throw "Already installed: $skillTarget" }
New-Item -ItemType Directory -Path (Split-Path $skillTarget) -Force | Out-Null
Copy-Item -LiteralPath './skills/stop-writing-tests' -Destination $skillTarget -Recurse
```

For Claude Code, change `.agents/skills/stop-writing-tests` to
`.claude/skills/stop-writing-tests` in the first line.

**macOS / Linux — Codex:**

```sh
skill_target="$HOME/.agents/skills/stop-writing-tests"
if [ -e "$skill_target" ]; then
  printf 'Already installed: %s\n' "$skill_target"
else
  mkdir -p "$(dirname "$skill_target")" &&
    cp -R ./skills/stop-writing-tests "$skill_target"
fi
```

For Claude Code, use `$HOME/.claude/skills/stop-writing-tests` instead.
For one project, copy the folder into that project's `.agents/skills/` (Codex)
or `.claude/skills/` (Claude Code), rather than your personal directory.

To update a manual installation, review the new `SKILL.md` and replace the
installed copy. To uninstall it, remove only the skill folder you installed.

Paths follow the official [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills)
and [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

</details>

Automatic selection depends on your agent and other instructions. Explicitly
invoke the skill when you want it applied; if it is missing from the selector,
start a fresh session. User requests and repository testing requirements still
apply. The installed skill is a single Markdown file with no runtime dependencies.

## Same task. Smaller aftermath.

**Task:** Rename an internal configuration attribute. Keep the public config
format and behavior unchanged; existing tests already exercise the affected path.

| Without the discipline | With `stop-writing-tests` |
| --- | --- |
| Rename the attribute | Rename the attribute |
| Add near-duplicate unit tests | Inspect the existing coverage |
| Add an integration harness | Run the relevant checks |
| Invent compatibility cases | Report the result and stop |
| Expand fixtures for those cases | No new test: no new evidence gap |

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

## Why another testing skill?

There is real overlap with existing work. This project does not claim to have
invented the question “does this test earn its place?”

| Project | Emphasis |
| --- | --- |
| [test-guard](https://github.com/amElnagdy/guard-skills/tree/master/skills/test-guard) | Primarily reviews generated tests; also supports upfront use and already asks what distinct bug each test catches. |
| [testing-skill](https://github.com/nickperkins/testing-skill) | Chooses testing layers and controls duplication, brittle assertions, and E2E scope. |
| [Superpowers TDD](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) | Organizes implementation around a failing test and the red/green/refactor cycle. |
| **stop-writing-tests** | A small, upfront decision about expanding test assets during ordinary coding tasks, with paired cases to check both restraint and necessary coverage. |

The distinction is scope and packaging, not an exclusive testing principle.
It can fit a TDD workflow: reuse a failing regression when one exists, write a
focused one when missing, and follow the project's required process.
See [research notes](evals/RESEARCH.md) for sources and boundaries.

## Does it work?

**Behavioral effectiveness has not yet been benchmarked.**

The repository includes runnable Python fixtures, evaluator-only acceptance
checks, reference edits, and a protocol comparing three conditions:

- No added testing instruction.
- One sentence asking for proportionate tests.
- The full skill.

Paired cases change the coverage or contract while keeping the task similar.
Correctness and missed regressions come before test counts. Added lines are a
descriptive metric, not a score to minimize.

See [the eval guide](evals/README.md) to reproduce fixture checks or run your own
agent comparison. Local fixture validation does not establish model behavior,
automatic activation, or a percentage improvement.

## Contributing

A useful contribution is a small reproducible case where the skill adds needless
tests, misses necessary protection, invents a requirement, or slows work down.
Include the task, relevant existing coverage, agent/model version, transcript,
and diff. Remove secrets and private code. Prefer a demonstrated failure over
another universal rule.

## License

[MIT](LICENSE).
