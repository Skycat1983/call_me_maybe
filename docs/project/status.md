# Project Status

Last reviewed: 2026-11-12

## Current objective

Review the successful explicit-CPU SDK evidence and understand prompt context before defining application architecture.

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

## In progress

- Discuss the waypoint 007 evidence in voice mode.

## Next

1. Explain the encode tensor, decode return values, and logits vector.
2. Explain why a bare prompt produced natural-language continuation tokens.
3. Decide what function definitions and output context a prompt must contain.
4. Record the prompt-design discussion before running another model probe.
5. Define component boundaries after the prompt responsibility is understood.

## Blockers

- No blocker for explicit-CPU learning experiments.
- Default/automatic device loading remains open as issue `I-003`.

## Active references

- [Documentation index](../index.md)
- [Requirements overview](../requirements/overview.md)
- [Task plan](tasks.md)
- [Learning log](../learning/index.md)
- [Open questions](questions.md)
- [Known issues](issues.md)
