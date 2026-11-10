# Project Status

Last reviewed: 2026-11-10

## Current objective

Choose and run a controlled follow-up to the first model-construction failure before defining the application architecture.

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

## In progress

- Discuss the waypoint 006 evidence and choose the next controlled experiment.

## Next

1. Discuss whether to test explicit CPU, supplied dependency versions, or
   `accelerate` first.
2. Run only the selected controlled experiment.
3. If construction succeeds, continue encode/decode, tokenizer, and logits
   observations.
4. Record the result in waypoint 007.
5. Define component boundaries only after SDK behavior is understood.

## Blockers

- Issue `I-003`: default model construction stops at the Transformers
  device-map check because `accelerate` is unavailable.

## Active references

- [Documentation index](../index.md)
- [Requirements overview](../requirements/overview.md)
- [Task plan](tasks.md)
- [Learning log](../learning/index.md)
- [Open questions](questions.md)
- [Known issues](issues.md)
