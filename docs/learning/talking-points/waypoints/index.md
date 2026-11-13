# Waypoint Talking Points

- Kind: Chronological discussion index
- Status: Current
- Last reviewed: 2026-11-13

Waypoint talking points prepare voice discussions about completed rounds of
work. The full chronological evidence remains in `docs/learning/waypoints/`.

## Available discussions

| Waypoint | Talking points | Theme |
|---|---|---|
| 001 | [Repository and source files](001-repository-and-source-files.md) | Git, remotes, ignored files, extraction, and source artifacts |
| 002 | [Requirements and documentation](002-requirements-and-documentation.md) | Requirement extraction and human-centered documentation |
| 003 | [Tooling and storage](003-tooling-and-storage.md) | uv, dependencies, lockfiles, Make, environments, and caches |
| 004 | [Supplied data and LLM SDK](004-supplied-data-and-llm-sdk.md) | Data contracts, model loading, tokens, logits, imports, and constrained decoding |
| 005 | [Environment repair and cache placement](005-environment-and-cache-placement.md) | Installed environments, package caches, model caches, and reproducibility |
| 006 | [First SDK probe](006-first-sdk-probe.md) | Constructor failure, dependency versions, device mapping, and experiment choice |
| 007 | [Explicit-CPU SDK probe](007-explicit-cpu-sdk-probe.md) | Successful loading, token tensors, decoding, tokenizer files, and logits |
| 008 | [Editor navigation and environment storage](008-editor-navigation-and-environment-storage.md) | Interpreter selection, `/tmp` storage, Pylance, and Go to Definition |
| 009 | [Project configuration and lockfile](009-project-configuration-and-lockfile.md) | TOML provenance, dependency categories, uv resolution, and synchronization |

Waypoint 010 is a [maintenance milestone](../../waypoints/010-2026-11-13-talking-points-architecture.md),
not a subject selected for voice discussion.

## How to use a waypoint discussion

Tell the agent:

> Read the selected companion and its linked chronological waypoint. Use its
> thematic links for current explanations. Ask one question at a time and help
> me explain what changed, what evidence supports it, and what remains open.

## Creating the next companion

When a waypoint will support a useful voice discussion, use the
[waypoint template](../templates/waypoint-talking-point.md). New files belong
in this directory and use `NNN-short-theme.md` names. Maintenance-only
waypoints do not require a companion.

## Related learning

- [Talking-points hub](../index.md)
- [Thematic discussions](../themes/index.md)
- [Chronological learning log](../../index.md)
- [Maintenance guide](../maintenance.md)
