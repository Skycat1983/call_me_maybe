# Talking Points 003: Tooling and Storage

Companion waypoint:
[003 — Tooling and storage](../waypoints/003-2026-11-06-tooling-and-storage.md)

## Agent preparation

Read the companion waypoint, the root `pyproject.toml`, and the `Makefile`.
Explain the role of each tool before discussing commands. Do not run dependency
installation during a voice discussion unless explicitly requested.

## Short recap

The root project was configured with application and development dependencies,
the local SDK was registered as a path dependency, a lockfile and Makefile
were created, and safe cache cleanup reduced home usage from 97% to 60%.

## Key concepts to discuss

1. `pyproject.toml` as project and dependency metadata.
2. `uv` as an external environment/package manager.
3. Runtime versus development dependencies.
4. Local path dependencies.
5. What a lockfile guarantees.
6. What a virtual environment isolates.
7. Why the Makefile wraps commands already provided by `uv`.
8. Reproducible dependencies versus disposable caches.

## Discussion prompts

- Why is `uv` not listed as a dependency inside the environment it manages?
- What is the difference between `pydantic` and `pytest` in this project?
- How does `[tool.uv.sources]` connect the root project to `llm_sdk/`?
- What information does `uv.lock` preserve?
- What would happen if the lockfile were deleted and dependencies resolved
  again later?
- Why does the SDK bring in large PyTorch/CUDA packages?
- Which Makefile targets are mandatory, and what does each wrap?
- How did we distinguish safe caches from unique personal or project data?

## Understanding checks

Ask the learner to classify:

- Pydantic: runtime dependency.
- NumPy: runtime dependency.
- Local `llm-sdk`: runtime dependency and local path source.
- Flake8, Mypy, pytest: development dependencies.
- `.venv`: generated environment, ignored by Git.
- `uv.lock`: reproducibility artifact, committed to Git.
- npm cache: reproducible cache, safe to remove.
- Source code and browser bookmarks: unique data, not cache cleanup targets.

## Likely misconceptions

- A lockfile records resolved versions; it does not contain installed package
  files.
- A virtual environment can be deleted and recreated, but recreation may be
  expensive.
- Removing caches may cause future downloads but should not remove source.
- `uv lock` and `uv sync` are different: resolving a lockfile does not prove
  every package is installed.
- A Makefile is a command interface, not a Python dependency manager.

## Current issue to discuss

The current `.venv` contains several dependencies but not `transformers`.
This demonstrates the distinction between a valid lockfile and a completely
synced environment. See
[`I-001`](../../project/issues.md#i-001-incomplete-project-environment).

## Successful session outcome

The learner can explain the relationship among `pyproject.toml`, `uv.lock`,
`.venv`, `uv sync`, the local SDK, and the Makefile, and can distinguish
reproducible cache data from unique data.
