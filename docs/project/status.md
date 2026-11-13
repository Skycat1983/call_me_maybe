# Project Status

Last reviewed: 2026-11-13

## Current objective

Understand the first strict Pydantic input models, then implement JSON file
loading and clear validation errors without involving the LLM.

## Completed

- Initialized the Git repository and connected it to GitHub.
- Extracted the supplied SDK and input data.
- Kept the PDF and original ZIP archives local-only.
- Extracted and condensed the project PDF.
- Archived the consolidated subject as a traceable source document.
- Split mandatory requirements into focused working documents.
- Added a documentation index and evaluation checklist.
- Added the root project configuration and dependency lockfile.
- Added Pydantic, NumPy, and the local SDK as project dependencies.
- Added Flake8, Mypy, and pytest as development dependencies.
- Added the required Makefile targets.
- Extended `.gitignore` for the virtual environment, caches, and generated output.
- Inspected the demonstration prompts and function definitions.
- Documented the SDK's imports, construction, public methods, state, tokens,
  and logits.
- Established numbered learning waypoint logs with detailed questions and
  answers.
- Added open-question and known-issue registers.
- Relocated the project environment and re-downloadable caches to `/tmp`.
- Completed dependency synchronization and verified the public SDK imports.
- Removed the incomplete local `.venv`, restoring home usage to 66%.
- Recorded the repair and storage model in waypoint 005.
- Added and validated a reusable public-interface SDK probe.
- Reproduced and documented the first model-construction failure.
- Loaded Qwen successfully with explicit CPU selection.
- Observed real encode/decode behavior, tokenizer files, and next-token logits.
- Resolved the initial tokenizer-file and decode-shape questions.
- Removed a newly recreated 1.1 GB local `.venv`, restoring home usage from
  99% to 77%.
- Linked the conventional `.venv` path to the real `/tmp` environment.
- Added project-level uv cache settings and VS Code workspace configuration.
- Verified definition-source paths and documented API discovery through type
  annotations, hover information, completion, and Go to Definition.
- Traced every root dependency category to the subject, supplied SDK, or a
  documented development choice.
- Documented how uv generated the 102-package lock and how `uv sync` uses it.
- Answered the learner's marked Makefile and SDK-probe questions inline.
- Added a living full-flow SDK-probe guide covering control flow, class
  internals, variable values and shapes, ownership, and call boundaries.
- Established separate chronological and thematic talking-points paths.
- Added talking-points indexes, maintenance rules, and reusable templates.
- Added a root `AGENTS.md` so future agents follow the same learning-first and
  documentation-maintenance conventions.
- Recorded the architecture decision and migration phases in waypoint 010.
- Moved chronological companions 001–009 into their dedicated directory.
- Moved the living SDK guides into an LLM-SDK theme, split them into focused
  documents, and added direct reading routes by goal and depth.
- Added a Python-tooling theme connecting configuration, uv, Make, storage,
  imports, and editor navigation.
- Removed the unnecessary architecture discussion companion so voice sessions
  stay focused on project substance.
- Created the first production `src` package and strict Pydantic models for
  prompt inputs, function definitions, and declared value types.
- Resolved Q-002 with initial `string`, `number`, and `boolean` support.
- Added 13 focused tests covering supplied examples and representative invalid
  structures; the new production and test code passes focused pytest, Flake8,
  Mypy, and compilation checks.
- Repaired the local SDK probe's dynamic `argparse` return annotation without
  changing runtime behavior.
- Extended issue I-002 with the supplied SDK's repository-wide Mypy findings.
- Added the living input-validation theme and Waypoint 011 discussion guide.

## In progress

- Discuss Waypoint 011 and trace how raw dictionaries become nested validated
  model instances.

## Next

1. Use the [Waypoint 011 discussion](../learning/talking-points/waypoints/011-pydantic-input-models.md)
   for the completed implementation round.
2. Use the [input-validation theme](../learning/talking-points/themes/input-validation/index.md)
   for Pydantic concepts, code, tests, and current boundaries.
3. Implement JSON loaders for prompts and function definitions.
4. Add tests for missing files, invalid JSON, wrong top-level values, invalid
   list items, and successful loading.
5. Add the CLI entry point only after the loading boundary has clear errors.

## Blockers

- No blocker for explicit-CPU learning experiments.
- Default/automatic device loading remains open as issue `I-003`.
- New application code passes focused static checks. Repository-wide Flake8
  and Mypy remain blocked by the supplied-SDK findings in issue `I-002`.

## Active references

- [Documentation index](../index.md)
- [Requirements overview](../requirements/overview.md)
- [Task plan](tasks.md)
- [Learning log](../learning/index.md)
- [Talking-points hub](../learning/talking-points/index.md)
- [Open questions](questions.md)
- [Known issues](issues.md)
