# Waypoint 003: Tooling and Storage

Date: 2026-11-06  
Stage: Development environment  
Status: Complete, with one later-discovered environment issue

## Purpose

Configure the root Python project and required commands, then recover enough
profile storage for model-related development.

## Topics covered

- Root `pyproject.toml` structure.
- Direct, transitive, and development dependencies.
- The role of `uv`.
- Local path dependencies.
- Lockfiles and reproducible environments.
- Required Makefile commands.
- Virtual-environment and application-cache storage.

## Progress made

- Created the root `pyproject.toml`.
- Declared `numpy`, `pydantic`, and the local `llm-sdk` as application
  dependencies.
- Declared Flake8, Mypy, and pytest as development dependencies.
- Configured `llm-sdk` as a local path source.
- Generated a root `uv.lock` resolving 102 packages.
- Added required Makefile targets:
  - `install`;
  - `run`;
  - `debug`;
  - `clean`;
  - `lint`.
- Added optional `lint-strict` and `test` targets.
- Extended `.gitignore` for `.venv`, caches, and `data/output/`.
- Audited a 97%-full home filesystem.
- Removed obsolete Codex data, npm/npx caches, Slack and VS Code caches,
  application logs, the NVM download cache, and all unused Cursor data.
- Reduced home usage from 97% to 60%, leaving approximately 1.9 GB free.

## Questions and answers

### Should `uv` be listed as a project dependency?

No. `uv` is the external tool that creates and manages the environment. The
packages installed into that environment belong in `dependencies` or a
development dependency group; the environment manager itself does not.

### Why is `llm-sdk` declared in both dependencies and `tool.uv.sources`?

The dependency list states that the application requires a package named
`llm-sdk`. The source table tells `uv` to obtain that package from the local
`llm_sdk/` directory rather than a public package registry.

### Why is the lockfile important?

`pyproject.toml` expresses allowed dependency ranges. `uv.lock` records the
specific resolved package graph so repeated installations use consistent
versions.

### Why add a Makefile if `uv` already provides commands?

The subject requires particular Makefile targets. It also gives humans and
the evaluator stable project-level commands without requiring them to
remember every underlying flag.

### Why did the virtual environment become so large?

The local SDK depends on PyTorch and model tooling. The resolved environment
includes large numerical and CUDA-related binaries. Those are dependencies,
not project source code.

### Which storage was safe to clean?

Re-downloadable caches, an obsolete Codex release, logs, and unused Cursor
data were safe because they were not unique project or personal documents.
The active Codex version, current project files, browsers, and Node runtime
were preserved.

## Evidence and experiments

The locked top-level graph included:

```text
call-me-maybe
├── llm-sdk
├── numpy
├── pydantic
├── flake8
├── mypy
└── pytest
```

Filesystem usage after cleanup:

```text
home size: 4.7 GB
used:      2.8 GB
available: 1.9 GB
usage:     60%
```

## Decisions

- Keep `uv` external to application dependencies.
- Use the supplied SDK as a local path dependency.
- Keep runtime and development dependencies separate.
- Preserve the project virtual environment because it is needed for future
  work.
- Remove only reviewed storage targets with known consequences.

## Later note

Waypoint 004 found that the virtual environment is not fully synchronized:
`transformers` is absent even though it is locked as an SDK dependency. See
issue `I-001`.

## Documents created or updated

- `pyproject.toml`
- `uv.lock`
- `Makefile`
- `.gitignore`
- `docs/project/status.md`
- `docs/project/tasks.md`

## Next step

Inspect the supplied data and SDK before writing application code.
