# Learning and Progress Log

This section records how the project develops and what is learned at each
meaningful waypoint.

## How the record is organized

The documentation has two complementary layers:

1. **Waypoint logs** preserve the chronological learning journey: what we
   worked on, questions asked, answers reached, evidence gathered, decisions
   made, and what should happen next.
2. **Thematic documents** hold the current reusable explanation of a subject.
   Requirements live in `docs/requirements/`, canonical technical facts in
   `docs/reference/`, living conversational guides in
   `docs/learning/talking-points/themes/`, and future implementation designs
   in `docs/design/`.

A waypoint should link to the thematic pages it created or changed. Thematic
pages should link back to a waypoint when historical context matters.

## Waypoints

| ID | Date | Theme | Main outcome |
|---|---|---|---|
| [001](waypoints/001-2026-11-06-repository-and-source-files.md) | 2026-11-06 | Repository and source files | GitHub repository initialized; supplied files extracted and local-only artifacts handled. |
| [002](waypoints/002-2026-11-06-requirements-and-documentation.md) | 2026-11-06 | Requirements and documentation | PDF converted into a navigable working specification. |
| [003](waypoints/003-2026-11-06-tooling-and-storage.md) | 2026-11-06 | Tooling and storage | Root dependency configuration and Makefile added; profile storage cleaned. |
| [004](waypoints/004-2026-11-10-supplied-data-and-llm-sdk.md) | 2026-11-10 | Supplied data and LLM SDK | Data contracts and the SDK's public interface explained; first runtime issues identified. |
| [005](waypoints/005-2026-11-10-environment-repair-and-cache-placement.md) | 2026-11-10 | Environment and cache placement | Complete environment moved to `/tmp`; SDK imports verified and home space restored. |
| [006](waypoints/006-2026-11-10-first-sdk-probe.md) | 2026-11-10 | First SDK runtime probe | Default model construction reproduced an `accelerate`/device-map failure before inference. |
| [007](waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md) | 2026-11-12 | Explicit-CPU SDK probe | Model loaded; encode/decode, tokenizer files, and one logits vector were observed. |
| [008](waypoints/008-2026-11-12-editor-navigation-and-environment-storage.md) | 2026-11-12 | Editor navigation and environment storage | Accidental local environment removed; VS Code navigation retained through a `/tmp`-backed `.venv` link and workspace settings. |
| [009](waypoints/009-2026-11-13-project-configuration-and-lockfile.md) | 2026-11-13 | Project configuration and lockfile | Direct dependencies traced to requirements; uv lock generation and synchronization documented; inline learner questions answered. |
| [010](waypoints/010-2026-11-13-talking-points-architecture.md) | 2026-11-13 | Talking-points architecture | Chronological discussions separated from living thematic learning; navigation, maintenance rules, templates, and agent instructions established. |

The next waypoint ID is **011**.

## Current registers

- [Open questions](../project/questions.md): unresolved questions that require
  investigation, an experiment, or a design decision.
- [Known issues](../project/issues.md): observed and reproducible problems.
- [Project status](../project/status.md): immediate objective and next actions.
- [Project tasks](../project/tasks.md): implementation work by milestone.
- [Learning roadmap](roadmap.md): the intended sequence of concepts and work.
- [Talking-points hub](talking-points/index.md): chronological voice-mode
  discussions and living topic-centered learning routes.

## Current thematic documents

- [Python project tooling](talking-points/themes/python-tooling/index.md)
- [LLM SDK and `inspect_sdk`](talking-points/themes/llm-sdk/index.md)
- [Requirements overview](../requirements/overview.md)
- [Input/output contract](../requirements/input-output-contract.md)
- [Constrained decoding requirements](../requirements/constrained-decoding.md)
- [LLM SDK reference](../reference/llm-sdk.md)
- [Python import resolution](../reference/imports.md)

## When to create a waypoint

Create a new waypoint when at least one of these is true:

- The main objective changes.
- A new technical theme is introduced.
- A meaningful experiment is completed.
- An implementation milestone is reached.
- A group of related questions has been answered.
- A decision materially changes the planned design.

Do not create a waypoint for a spelling correction or a single trivial command.

## Waypoint format

Each waypoint should contain:

```markdown
# Waypoint NNN: Title

Date:
Stage:
Status:
Voice discussion:

## Purpose
## Topics covered
## Progress made
## Questions and answers
## Evidence and experiments
## Decisions
## Open questions or issues
## Documents created or updated
## Next step
```

Questions and answers should be detailed enough that the reasoning can be
understood later without reconstructing the original conversation.

## Maintenance rules

1. Do not rewrite history simply because the design later changes. Add a note
   pointing to the newer waypoint.
2. Correct factual errors when discovered and record the correction in the
   newer waypoint.
3. Keep answered questions in the waypoint where they were answered.
4. Copy only unresolved questions into `docs/project/questions.md`.
5. When an open question is resolved, update its register entry with the
   resolving waypoint and move durable knowledge into a thematic document.
6. Record observed defects in `docs/project/issues.md`, not as vague tasks.
7. Avoid duplicating full explanations across files; link to the canonical
   thematic page.
8. Use filenames in the form `NNN-YYYY-MM-DD-short-theme.md`.
9. Add a companion file under `talking-points/waypoints/` when a waypoint is
   useful for a planned voice discussion, and link the two files in both
   directions. A maintenance-only waypoint may omit one.
10. Maintain living topic-centered guides under `talking-points/themes/` and
    follow the [talking-points maintenance guide](talking-points/maintenance.md)
    when creating, splitting, or moving them.
