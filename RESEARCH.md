# Research notes

Checked 2026-09-17. These are design inputs, not effectiveness endorsements.
The skill and fixtures were written for this project; no upstream code or skill
body is vendored.

## Format and installation

- [Agent Skills specification](https://agentskills.io/specification): a folder
  with `SKILL.md`, required `name` and `description`, and optional resources.
  The name must match the folder. This package uses a single instruction file.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills): local
  Codex discovery includes `~/.agents/skills` and project `.agents/skills`.
  Explicit selection and implicit matching are distinct. Optional UI metadata
  and plugin distribution exist; neither is necessary for this standalone skill.
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills):
  personal skills use `~/.claude/skills`, project skills `.claude/skills`, and
  `/skill-name` supports explicit invocation. No Claude-specific frontmatter is
  needed here.

- [Vercel Labs: Skills CLI](https://github.com/vercel-labs/skills): supports
  GitHub repositories and local directories, skill discovery with `--list`,
  agent selection with `--agent`, and personal installation with `--global`.
  The root README uses this installer as the main path; no npm package needs to
  be published for this skill. Node.js/npm is needed for the installer only.

Remote commands target `emerardd/stop-writing-tests` and require GitHub publication;
local installation uses `npx skills add . --skill stop-writing-tests`. Manual
copy remains a folded fallback. Native host discovery remains a separate smoke
test; successful CLI discovery or copying is not proof of activation.

## Related approaches

- [amElnagdy/guard-skills: test-guard](https://github.com/amElnagdy/guard-skills/blob/master/skills/test-guard/SKILL.md)
  is the closest overlap. It primarily targets generated-test review, but also
  supports upfront use. It already asks for the distinct bug a new test detects
  and requires tests to justify their existence. Claims that it only evaluates
  how tests are written would misrepresent it. Our narrower scope is deciding
  whether to grow test assets during the coding task, preserving existing
  protection and verifying that restraint does not miss needed regressions.
- [nickperkins/testing-skill](https://github.com/nickperkins/testing-skill)
  emphasizes the testing pyramid, choosing layers, rejecting redundant coverage,
  and limiting E2E permutations. Our decision does not prescribe a testing pyramid
  or framework and includes the option to add no persistent test asset.
- [obra/superpowers: TDD](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md)
  emphasizes observing a failing test before implementation and the
  red/green/refactor loop. Our concern is the incremental value and scope of test
  additions. Repository-mandated TDD still applies.

These sources cover anti-bloat review, test quality and levels, regression
discipline, and test-first workflows. This is a bounded comparison, not a claim
that all competing projects have been exhausted or that the doctrine is novel.

## Hypothesis to measure

A short upfront decision rule may reduce redundant test assets and invented
contracts without reducing correctness or missing necessary regression coverage.
Compare it with both an untreated agent and a one-sentence instruction; do not
assume a longer skill outperforms the shorter baseline. Test host activation
separately from the efficacy of the loaded instructions.
