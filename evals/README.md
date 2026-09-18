# Evaluate the decision, not the line count

This is a small, inspectable evaluation set, not a claim of measured model
improvement. It contains **14 Python mini-projects**, uses the standard library,
and requires Python 3.10 or later. Only the evaluator uses Python; installing the
skill requires no runtime.

## What is in a case?

```text
cases/<case>/
  task.md          The user's request
  workspace/       Starting code, existing tests, and project documentation
  case.json        Evaluator-only expectations and review criteria
  oracle.py        Evaluator-only behavioral acceptance subset
  reference/       One acceptable edit, overlaid on workspace for fixture checks
```

The agent gets **only the workspace and task prompt**, plus the treatment for its
condition. Keep `case.json`, `oracle.py`, and `reference/` out of its context and
accessible filesystem. These are public fixtures, not secret or contamination-proof
benchmarks. Never run the evaluated agent in this repository root.

Reference edits are illustrative solutions, not exact patches an agent must
match. Case 11 intentionally has no implementation: a focused clarification is
the correct response until the product decision is supplied.

## Cases and pairs

| Case | Expected decision | What changes the decision? |
| --- | --- | --- |
| 01 internal rename | Reuse coverage | Public greeting behavior is covered. |
| 02 docs only | No test additions | Fix prose; appropriate document verification suffices. |
| 03 internal config rename | Reuse coverage | Keep the public key; existing tests exercise the path. |
| 04 pure refactor | Reuse coverage | Existing total and empty-input checks protect behavior. |
| 05 cache, regression missing | Add focused regression | Expiration equality is uncovered. |
| 06 cache, regression present | Reuse failing regression | Same bug and request as 05, but coverage already exists. |
| 07 new public behavior | Add focused coverage | The request introduces an observable status label. |
| 08 undefined edge, rename only | No speculative policy | Empty-input behavior is not required to perform the rename. |
| 09 defined edge | Add focused coverage | Same starting parser, but an empty-input default is authorized. |
| 10 internal branches | Reuse coverage | Existing checks cover the access policy including denial. |
| 11 consequential ambiguity | Ask a focused question | The task requires an empty-input decision with no agreed outcome. |
| 12 explicit test request | Add the requested test | User intent takes precedence over the default. |
| 13 public config change | Add contract coverage | Unlike 03, the public key and precedence change. |
| 14 repository requirement | Follow the repo | Same rename as 01, plus a documented coverage requirement. |

The cases cover restraint, missing regression coverage, public contracts,
speculative behavior, security-policy preservation, and instruction precedence.
They do not establish performance on large repositories, concurrency, property
testing, complex integration boundaries, or other languages.

## Check the fixtures first

From the repository root:

```sh
python evals/run.py check-fixtures
python evals/run.py list
```

Use `python3` if that is your Python 3 executable. The checker runs existing tests
and acceptance checks before and after overlaying the reference edits, in temporary
copies. Some original versions **must fail**: case 06 already contains a failing
regression, and the original code in cases 05, 06, 07, 09, and 13 fails its updated
behavioral acceptance checks. The checker also verifies that reference tests for
those five cases reject the original implementation.

Passing fixture validation establishes that the examples and checks are executable.
It does **not** mean a model followed the skill.

## Compare three conditions

Use the same agent, exact model/version, reasoning setting, tools, runtime,
permissions, and starting files. Start a fresh session for **every** case,
condition, and repetition. Keep unrelated testing skills, custom instructions,
memories, and previous answers out of the environment; record anything you cannot
isolate. Randomize condition order and run multiple repetitions (five per case and
condition is a reasonable initial plan, not a power calculation).

| Condition | Added instruction |
| --- | --- |
| `baseline` | None. |
| `one-line` | Avoid redundant tests; reuse existing coverage and add the smallest test needed for a real coverage gap. |
| `skill` | The complete `SKILL.md`, supplied explicitly in the prompt. |

Prepare separate runs, for example:

```sh
python evals/run.py prepare 05-cache-missing --condition baseline --output .eval-runs/cache-baseline-1
python evals/run.py prepare 05-cache-missing --condition one-line --output .eval-runs/cache-one-line-1
python evals/run.py prepare 05-cache-missing --condition skill --output .eval-runs/cache-skill-1
```

Each output contains `workspace/`, `PROMPT.md`, and `run.json`. Preparation refuses
to overwrite an existing output. It makes no model call and installs nothing.

1. Copy the prepared `workspace/` into an isolated agent environment. Give the
   agent the text of `PROMPT.md` as its task, without the evaluator's other files.
2. Let it finish, or stop at a necessary clarification. For case 11, record the
   question and end the run without supplying a new policy. Use the same time or
   turn budget across conditions; count timeouts and failures, do not discard them.
3. Copy the resulting workspace back to that run's `workspace/`. Keep the
   transcript separately as `transcript.md` or the host's export. Do not put it
   inside `workspace/` where it would count as a code change.
4. Fill the nullable metadata in `run.json`: agent, model, reasoning, host version,
   repetition, elapsed seconds, and tokens if available. Preserve the generated
   case, condition, and content hashes. Unknown measurements stay `null`.
5. Inspect the result as below. Repeat for all cases and conditions.

**Codex and Claude Code:** both can perform this protocol by starting a fresh
task/session in the isolated workspace and pasting the generated prompt. For this
explicit-prompt comparison, do not also install the skill into the eval host:
that would contaminate the baseline. Native installation and discovery are tested
separately below. Host CLI automation is intentionally left out of this small
provider-independent harness.

## Inspect and score

`inspect` executes the submitted Python tests and imports the submitted code in
temporary copies. Run it on trusted eval output or inside your evaluation sandbox;
the helper is not a sandbox.

```sh
python evals/run.py inspect .eval-runs/cache-skill-1
```

It produces `changes.diff` and `report.json` with:

- Added test-file count and added/removed test-line counts, using documented path
  heuristics (`test*`, `tests/`, `fixtures/`, `snapshots/`, `conftest.py`). Counts
  include blank lines and comments and are sensitive to formatting and renames.
- Every changed file, including files outside those heuristics, for manual review.
- The submitted suite and independent acceptance-subset results, with output.
- Empty manual-review fields. It does not award a score for a smaller diff.

Review test helpers, parameter rows, snapshots, dependencies, and unusual file
names manually. The automated line count cannot detect them all. Renaming or
compressing tests should never earn an apparent improvement. `inspect` refuses to
overwrite a filled report; archive the old report before reinspecting a new edit.

Use the task, `case.json`, diff, and transcript to complete this rubric. Ideally
have a reviewer blind to condition grade anonymized artifacts first.

| Field | How to judge it |
| --- | --- |
| `task_correct` | All requested edits and preserved behavior are correct; for case 11, a focused question without an invented policy counts as success. Acceptance checks are only a subset. |
| `necessary_coverage_retained` | Required existing protection and needed new regression/contract evidence are present. Read assertions, not just test names. |
| `missed_required_regression` | True if a case requiring new protection has only a code fix or manual reproduction, or its added test cannot detect the relevant failure. |
| `redundant_tests` | Count additions with no worthwhile incremental evidence. Consider useful layer boundaries, reliability, and feedback speed. |
| `duplicate_coverage` | Count added scenarios repeating existing evidence without a justified benefit. This may overlap `redundant_tests`; do not add the counts together. |
| `invented_requirements` | Count unsupported behavior decisions frozen into code or assertions. |
| `unnecessary_infrastructure` | Count unjustified frameworks, dependencies, fixture layers, or harnesses. |
| `existing_protection_weakened` | True for unjustified deletion, skips, weakened assertions, or reduced thresholds. Authorized contract updates are assessed separately. |
| `verification_adequate` | Appropriate checks actually ran; failures and unavailable checks were reported honestly. Do not require code tests for a prose-only edit. |
| `per_addition_evidence` | For each new test/scenario, record its location, concrete failure, behavior source, existing-coverage gap, and verdict. |

For a new regression, transplant the added test onto the original implementation
in a disposable copy where feasible. It should fail because of the intended bug,
not an import failure or unrelated fixture error. A test passing on both versions
needs an explanation. New APIs may require a minimal compatible setup to make
this comparison meaningful. Never derive an oracle by copying the submitted
implementation.

Report correctness, coverage retention, and harmful omissions **before** counts or
costs. Compare paired cases and all three conditions. Publish raw sample sizes,
failure/timeout counts, model/settings, fixture and skill hashes, and per-case
results. Report uncertainty and avoid claiming unchanged correctness from a small
sample. Keep tokens and time as separate costs; do not reward verbosity or require
a four-question essay from the agent.

## Check native activation separately

In a clean Codex or Claude Code profile:

1. Follow the root README's copy instructions for that host.
2. Confirm the skill appears in its selector and explicitly invoke it on a copied
   case. Check the transcript shows it was loaded before test expansion.
3. In a separate fresh session, submit only the same task without mentioning the
   skill. Record whether the host selected it. Do not insert the skill manually
   and count that as automatic activation.
4. Include both a restraint case and a missing-regression case. Record host/model
   versions and whether other instructions affected the decision.

A skill that works when loaded can still fail to activate. Report those outcomes
separately. Nothing in this repository guarantees unconditional host enforcement.

## Current evidence

See [VALIDATION.md](VALIDATION.md) for local fixture and packaging checks,
[PILOT-2026-09-18.md](PILOT-2026-09-18.md) for the first pilot, and
[RUN-2026-09-18.md](RUN-2026-09-18.md) for a small run across all cases on one
model. There is no adequately powered model comparison yet. Please do not turn the README's
illustrative example into an efficacy claim.
