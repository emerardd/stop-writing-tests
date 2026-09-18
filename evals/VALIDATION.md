# Local validation record

Date: 2026-09-17. This records engineering checks, **not an agent benchmark**.

Environment: Windows, PowerShell 7.6.6, Python 3.12.14 for fixture checks,
Python 3.12.10 for smoke checks and the authoring validator, Git Bash 5.2.37.

| Check | Result | What it establishes |
| --- | --- | --- |
| Skill authoring `quick_validate.py` | Passed | Required frontmatter, naming, and supported fields are valid; no unfinished scaffold. |
| `python evals/run.py check-fixtures` | 14/14 cases matched expectations | Original suite/acceptance outcomes and reference suite/acceptance outcomes are executable and consistent with each manifest. |
| Reference tests on original implementations | Expected failures in 05, 06, 07, 09, 13 | The reference coverage detects the original missing behavior or regression. Other cases pass as declared. |
| Preparation, all three conditions | Passed | Identical starting workspaces; only the skill condition gets the complete skill; evaluator files are not copied into agent workspaces. |
| Inspection of original cache case | Suite passes, acceptance fails | Existing happy-path coverage does not detect the missing expiration boundary. |
| Inspection of reference cache fix | Both pass | Fixed behavior and its focused regression are executable. |
| Diff metrics | Passed controlled checks | Modifications inside an existing test file and a newly added test file are counted. |
| Overwrite protection | Passed | Existing run directories and review reports are not silently replaced. Invalid case selection is rejected. |
| README installation snippets | Passed in PowerShell and Git Bash for both agent paths | Copied skill bytes match the source and a second install preserves the existing target. Smoke checks used isolated substitute home directories, not personal settings. |
| Skills CLI 1.6.0 local discovery | Passed | `npx skills add . --list` found exactly one skill, `stop-writing-tests`. The check used a workspace-local npm cache; no skill was installed. |
| Relative documentation links | Passed | Repository-relative links resolve to existing files. |

## Not established

- GitHub installation from `emerardd/stop-writing-tests` has not been tested;
  it requires the repository to be published.

- No model ran the three-condition comparison. There are no efficacy percentages,
  measured token savings, or claims of unchanged task accuracy.
- Codex and Claude Code native skill discovery and implicit activation were not
  exercised. Paths and invocation are documented from official sources; copy
  validation alone does not prove host behavior.
- Shell snippets were exercised on Windows PowerShell and Git Bash, not native
  macOS or Linux. The Python helper was exercised on Python 3.12, not every
  supported Python version.
- Acceptance checks cover a behavioral subset. They do not automatically prove
  a rename occurred, documentation was corrected, ambiguity was surfaced, tests
  provide independent evidence, or existing protection was preserved. Those
  checks require the rubric and transcript/diff review.
- This is a small Python evaluation set, not evidence of effectiveness across
  languages or large production repositories.

## Reproduce

```sh
python evals/run.py check-fixtures
python evals/run.py prepare 05-cache-missing --condition baseline --output .eval-runs/validation-baseline
python evals/run.py inspect .eval-runs/validation-baseline
```

The last command should report a passing submitted suite and a failing acceptance
subset because no fix has been applied. It is a useful negative control, not a
failed agent run. To inspect the reference result, prepare another run, overlay
`cases/05-cache-missing/reference/` onto its workspace, and inspect that run.

See the [eval protocol](README.md) for actual model comparisons. Local smoke output
belongs under the ignored `.eval-runs/` directory and must not be published as
model evidence.
