# Documentation

This is the entry point for project documentation.

## Start here

| Need | Document |
|---|---|
| See the current state and immediate next step | [Project status](project/status.md) |
| Choose work to do | [Project tasks](project/tasks.md) |
| Review progress, questions, and answers | [Learning and progress log](learning/index.md) |
| See unresolved questions and known problems | [Open questions](project/questions.md) and [known issues](project/issues.md) |
| Understand the assignment | [Requirements overview](requirements/overview.md) |
| Check exact program inputs and outputs | [Input/output contract](requirements/input-output-contract.md) |
| Understand the central algorithm requirement | [Constrained decoding](requirements/constrained-decoding.md) |
| Prepare for review or submission | [Evaluation checklist](requirements/evaluation-checklist.md) |
| Consult the condensed source subject | [Subject v1.7 archive](archive/subject-v1.7-condensed.md) |

## Current documentation

### Requirements

These documents define what the project must do.

- [Overview](requirements/overview.md): objective, scope, and acceptance targets.
- [Implementation rules](requirements/implementation-rules.md): environment, dependencies, code quality, tooling, and repository constraints.
- [Input/output contract](requirements/input-output-contract.md): CLI, file formats, validation, and error behavior.
- [Constrained decoding](requirements/constrained-decoding.md): mandatory generation behavior.
- [Evaluation checklist](requirements/evaluation-checklist.md): final verification checklist with links to canonical requirements.

### Project management

These documents describe the work as it stands now.

- [Status](project/status.md): current objective, completed work, next actions, and blockers.
- [Tasks](project/tasks.md): work organized by milestone.
- [Open questions](project/questions.md): unresolved questions requiring evidence or decisions.
- [Known issues](project/issues.md): observed and reproducible problems.

### Learning and progress

- [Learning log index](learning/index.md): chronological waypoint navigation,
  recording rules, and links to thematic knowledge.
- [Learning roadmap](learning/roadmap.md): the explain-first sequence for the
  rest of the project.
- [Waypoint talking points](learning/talking-points/index.md): voice-mode
  discussion guides for every completed waypoint.
- [Latest waypoint](learning/waypoints/006-2026-11-10-first-sdk-probe.md):
  first model-construction probe, observed failure, evidence, and controlled
  follow-up options.

### Reference

- [LLM SDK](reference/llm-sdk.md): model loading, public methods, logits,
  tokenizer files, and private state.
- [Python imports](reference/imports.md): what the SDK imports and how `uv`
  makes dependencies importable.

### Archive

- [Condensed project subject, version 1.7](archive/subject-v1.7-condensed.md): the first-pass extraction of the supplied PDF. It is retained for traceability and is not the day-to-day working specification.

## Documentation to add when needed

Do not create these as empty placeholders. Add them once implementation produces meaningful content.

```text
docs/
├── design/
│   ├── architecture.md
│   ├── generation-pipeline.md
│   ├── validation-strategy.md
│   └── decisions.md
├── guides/
│   ├── setup.md
│   ├── running.md
│   ├── testing.md
│   └── troubleshooting.md
└── reference/
    ├── data-formats.md
    ├── glossary.md
    └── resources.md
```

Create a document when:

- `architecture.md`: component boundaries and data flow have been chosen.
- `generation-pipeline.md`: the implemented generation algorithm can be described.
- `validation-strategy.md`: validation responsibilities have been assigned.
- `decisions.md`: an important technical choice needs a durable explanation.
- A guide: a repeatable setup, run, test, or recovery procedure exists.
- A reference page: information is repeatedly needed during development.

## Maintenance rules

1. Give each fact one canonical home; link to it elsewhere.
2. Requirements state what must happen. Design documents explain how it is achieved.
3. Keep `project/status.md` brief and current.
4. Tasks are planned work; issues are observed defects.
5. Move resolved questions into a decision record when the answer affects the design.
6. Record learning and progress in numbered waypoint logs, not command-by-command activity.
7. Preserve source-derived documents in `archive/`; update working documents instead.
8. Use lowercase, hyphenated filenames.
