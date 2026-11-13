# Thematic Talking Points

- Kind: Living thematic index
- Status: Current
- Last reviewed: 2026-11-13

Thematic talking points explain subjects independently of when they were
encountered. They are living documents that can offer surface explanations,
theory, project application, detailed flows, and question-led discussions.

## Available themes

| Theme | Best for | Available routes |
|---|---|---|
| [LLM SDK and `inspect_sdk`](llm-sdk/index.md) | Understanding the supplied model wrapper, probe source, runtime behavior, tensors, decoding, tokenizer files, logits, and call flow | Quick summary, provenance, code walkthrough, observed results, detailed execution, variable ledger, and discussion questions |
| [Python project tooling](python-tooling/index.md) | Understanding TOML, uv, locks, installation, Make, `/tmp` environments, caches, imports, and editor navigation | Surface model, configuration and locking, command execution, storage, imports, editor navigation, and discussion questions |

## Planned reading routes

A mature theme index should let a learner choose among:

- a five-minute overview;
- general concepts and theory;
- application in this repository;
- detailed runtime or algorithm flow;
- question-led voice discussion.

Not every theme needs every route. Documents are created when meaningful
content exists, not as empty placeholders.

## Current structure

```text
themes/
├── python-tooling/
│   └── index.md
└── llm-sdk/
    ├── index.md
    ├── probe/
    │   ├── index.md
    │   ├── source-walkthrough.md
    │   ├── experiments-and-results.md
    │   └── questions-and-discussion.md
    └── runtime-flow/
        ├── index.md
        ├── command-and-entry.md
        ├── model-construction.md
        ├── encoding-and-decoding.md
        ├── tokenizer-files.md
        ├── logits-and-ranking.md
        └── variable-ledger-and-discussion.md
```

The original long SDK documents were split at meaningful learning boundaries.
The theme index preserves overview-to-detail routes without duplicating their
content.

## Creating a theme

Use the [theme-index template](../templates/theme-index.md) and
[thematic-topic template](../templates/thematic-topic.md). Follow the splitting
and navigation rules in the [maintenance guide](../maintenance.md).

## Related learning

- [Talking-points hub](../index.md)
- [Waypoint discussions](../waypoints/index.md)
- [Learning roadmap](../../roadmap.md)
- [Requirements](../../../requirements/overview.md)
- [Reference documentation](../../../index.md#reference)
