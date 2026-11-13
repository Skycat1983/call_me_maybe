# Project Status

Last reviewed: 2026-11-13

## Current objective

Use the substantive theme routes to discuss project configuration, the SDK
probe, and source-code flow. Then return to prompt and function-definition
context for the next focused experiment.

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

## In progress

- Choose a substantive discussion route: Python tooling and configuration, or
  the LLM SDK and `inspect_sdk.py` code flow.

## Next

1. Use the [Python-tooling theme](../learning/talking-points/themes/python-tooling/index.md)
   for dependencies, uv, locks, Make, storage, imports, or editor navigation.
2. Use the [LLM-SDK theme](../learning/talking-points/themes/llm-sdk/index.md)
   for probe provenance, source code, runtime results, model construction,
   tokens, decoding, tokenizer files, logits, or variable ownership.
3. Record questions or corrections that emerge from the discussion in the
   appropriate living theme or project register.
4. Return to function-definition and output context for the next prompt probe.

## Blockers

- No blocker for explicit-CPU learning experiments.
- Default/automatic device loading remains open as issue `I-003`.

## Active references

- [Documentation index](../index.md)
- [Requirements overview](../requirements/overview.md)
- [Task plan](tasks.md)
- [Learning log](../learning/index.md)
- [Talking-points hub](../learning/talking-points/index.md)
- [Open questions](questions.md)
- [Known issues](issues.md)
