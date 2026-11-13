# Theme: Python Project Tooling

- Kind: Thematic talking-point index
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: None

## Purpose

Use this theme to understand how the repository declaration, lockfile,
installed environment, Make commands, caches, imports, and editor navigation
fit together. The linked waypoint discussions contain the detailed questions
and answers already developed for each part.

## Five-minute mental model

```text
pyproject.toml
    human-authored project intent and direct dependencies
        |
        v
uv.lock
    uv-generated exact dependency resolution
        |
        v
uv sync / uv run
    installed environment under /tmp
        |
        v
selected Python interpreter
    imports packages and enables editor source navigation
```

The Makefile is a human-authored command menu around these tools. It exports
the project's `/tmp` storage locations and delegates the actual dependency or
Python work to uv, Flake8, Mypy, pytest, or Python.

## Choose a route

### Understand dependencies and the lockfile

Read [Project configuration and lockfile](../../waypoints/009-project-configuration-and-lockfile.md).
This is the most current explanation of:

- where each dependency declaration came from;
- direct, development, and transitive dependencies;
- the local `llm-sdk` source mapping;
- what uv decides and records;
- how `uv sync` creates an installed environment.

### Understand Make and the original tool setup

Read [Tooling and storage](../../waypoints/003-tooling-and-storage.md), then
inspect the [`Makefile`](../../../../../Makefile). Focus on the distinction
between a saved recipe and the program that recipe invokes.

### Understand environments and caches

Read [Environment repair and cache placement](../../waypoints/005-environment-and-cache-placement.md).
It separates:

- the installed project environment;
- uv's reusable package cache;
- Hugging Face's model cache;
- persistent repository files;
- disposable `/tmp` state.

### Understand imports and source navigation

Read [Editor navigation and environment storage](../../waypoints/008-editor-navigation-and-environment-storage.md)
and the canonical [Python import reference](../../../../reference/imports.md).
This route explains why selecting the correct interpreter enables imports,
hover information, completion, and Go to Definition without placing the large
environment in the profile filesystem.

### See tooling drive a real experiment

Use the [LLM-SDK runtime route](../llm-sdk/index.md#follow-the-complete-runtime-flow).
It traces `make inspect-sdk-cpu` through uv, Python, the local probe, the SDK,
and the model libraries.

## Responsibilities at a glance

| Item | Responsibility | Persistent? |
|---|---|---|
| `pyproject.toml` | Desired metadata, dependency constraints, and tool settings | Yes; authored and committed |
| `uv.lock` | Exact resolved package graph and distribution metadata | Yes; generated and committed |
| `Makefile` | Stable project commands and storage environment variables | Yes; authored and committed |
| `/tmp/call-me-maybe-venv` | Installed packages used by Python and the editor | Reproducible and disposable |
| `/tmp/call-me-maybe-uv-cache` | Reusable downloaded/built package data | Disposable |
| `/tmp/call-me-maybe-huggingface` | Downloaded model and tokenizer artifacts | Disposable |
| `.venv` link | Conventional editor-facing path to the real environment | Small, local, and reproducible |

## Question-led discussion

Ask the agent to choose one chain and let you narrate it first:

1. requirement → `pyproject.toml` → `uv.lock` → installed package;
2. Make target → uv command → Python process;
3. import statement → selected interpreter → installed source file;
4. cleared `/tmp` → recreated environment and caches;
5. direct SDK dependency → SDK metadata → transitive model dependencies.

The agent should correct one boundary at a time instead of presenting all of
the tooling as a single hidden action.

## Current project application

- The environment and large caches intentionally live under `/tmp` because
  profile storage is limited.
- Clearing `/tmp` is acceptable; `make install` and later model loading can
  recreate what is missing.
- uv itself is an external tool, not a dependency installed inside the
  environment it manages.
- `pyproject.toml` is human-authored; `uv.lock` is generated and should not be
  hand-edited.
- The root project declares `llm-sdk`; its source table points uv to the local
  `llm_sdk/` directory; the SDK's own metadata introduces Transformers,
  PyTorch, and related transitive packages.

## Related learning

- [Talking-points hub](../../index.md)
- [Thematic discussions](../index.md)
- [LLM SDK and `inspect_sdk`](../llm-sdk/index.md)
- [Implementation rules](../../../../requirements/implementation-rules.md)
- [Project status](../../../../project/status.md)
- [Learning roadmap](../../../roadmap.md)
