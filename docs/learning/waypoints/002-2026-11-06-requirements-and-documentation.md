# Waypoint 002: Requirements and Documentation

- Date: 2026-11-06
- Stage: Requirements analysis
- Status: Complete

Voice discussion: [Talking points 002](../talking-points/waypoints/002-requirements-and-documentation.md)

## Purpose

Turn the 21-page subject PDF into concise, searchable documentation organized
around the questions a developer will ask while working.

## Topics covered

- Extracting text from the PDF.
- Removing narrative material without losing requirements.
- Separating stable requirements, active project state, and historical source
  material.
- Organizing documentation for human navigation.
- Avoiding both one oversized document and many empty placeholders.

## Progress made

- Extracted all PDF text into a first-pass Markdown specification.
- Reduced approximately 4,300 words to approximately 1,700 while preserving
  implementation, validation, evaluation, and submission requirements.
- Preserved that document as
  `docs/archive/subject-v1.7-condensed.md`.
- Split working requirements into focused files:
  - overview;
  - implementation rules;
  - input/output contract;
  - constrained decoding;
  - evaluation checklist.
- Added `docs/index.md`.
- Added project status and task dashboards.
- Added a root README link to the documentation index.
- Committed the organized documentation in commit `8f10226`.

## Questions and answers

### Why not leave everything in one specification file?

One large file is useful for preservation but inefficient during development.
When implementing the CLI, the developer needs the input/output contract; when
working on token filtering, they need constrained-decoding requirements. Small
focused documents reduce search time and mental context switching.

### Why not create every possible document immediately?

Empty architecture, issue, troubleshooting, and decision documents create
navigation noise and imply knowledge that does not yet exist. A document
should be created when its subject has meaningful content.

### What is the difference between requirements and design?

Requirements describe what the solution must do. Design documentation
explains how this implementation will satisfy those requirements. Keeping
them separate prevents an early implementation idea from being mistaken for
an assignment rule.

### Where should current work be recorded?

`docs/project/status.md` should show the immediate objective and next actions.
`docs/project/tasks.md` should organize planned work by milestone. Historical
source extraction remains in `docs/archive/`.

### How should a human enter the documentation?

The root README points to `docs/index.md`. The index answers practical
questions such as “What should I do next?”, “What is the exact output
contract?”, and “What will the evaluator check?”

## Decisions

- Use one archived condensed subject as the traceable source snapshot.
- Make the smaller requirement files the working source of truth.
- Organize navigation by human need rather than the PDF's chapter order.
- Link instead of duplicating full explanations.
- Add future documentation only when content exists.

## Open questions or issues

- The implementation architecture was intentionally deferred until the SDK
  and data had been inspected.

## Documents created or updated

- `docs/index.md`
- `docs/archive/subject-v1.7-condensed.md`
- `docs/requirements/overview.md`
- `docs/requirements/implementation-rules.md`
- `docs/requirements/input-output-contract.md`
- `docs/requirements/constrained-decoding.md`
- `docs/requirements/evaluation-checklist.md`
- `docs/project/status.md`
- `docs/project/tasks.md`
- `README.md`

## Next step

Create the root dependency configuration and required development commands.
