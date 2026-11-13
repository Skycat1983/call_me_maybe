# Talking Points 009: Project Configuration and Lockfile

Companion waypoint:
[009 — Project configuration and lockfile](../../waypoints/009-2026-11-13-project-configuration-and-lockfile.md)

## Agent preparation

Read:

- the companion waypoint;
- `pyproject.toml`;
- the root `uv.lock` header and first project entries;
- `llm_sdk/pyproject.toml`;
- the Makefile and its inline learner questions;
- `experiments/inspect_sdk.py` and its inline learner questions;
- [implementation rules](../../../requirements/implementation-rules.md).

Keep authored intent separate from generated resolution. Ask the learner to
reason from the declarations before discussing individual locked packages.

## Short recap

Humans authored the root project declaration from the subject, supplied SDK,
and development choices. uv followed those declarations recursively and
generated a 102-package lock. `uv sync` then uses the declaration and lock to
create a matching environment under `/tmp`.

## Conversation order

1. What belongs in `pyproject.toml`.
2. Where each direct dependency came from.
3. Direct versus transitive versus development dependencies.
4. Why `llm-sdk` appears in both dependencies and the uv source table.
5. What uv resolves and records in `uv.lock`.
6. What `uv sync` changes on disk.
7. How Make passes storage configuration to uv and Python.
8. How source comments and real docstrings answer different kinds of
   questions.
9. File structure versus editor syntax highlighting.

## Core comparison

| Item | Authored by | Main meaning |
|---|---|---|
| `pyproject.toml` | Humans | Desired project metadata, dependency constraints, and tool settings |
| `llm_sdk/pyproject.toml` | Supplied SDK author | SDK package metadata and its own direct dependencies |
| `uv.lock` | uv | Exact resolved dependency graph and distribution metadata |
| `/tmp/call-me-maybe-venv` | Created/synchronised by uv | Installed environment used to run and inspect the project |
| Makefile | Humans | Stable commands and environment variables around the underlying tools |

## Discussion prompts

- Which root dependencies were explicitly required by the subject?
- Which version bounds were our choices rather than subject requirements?
- Why are PyTorch and Transformers absent from the root dependency list?
- How does uv discover that the application nevertheless needs them?
- Why does `llm-sdk` need both a dependency entry and a source entry?
- What information can uv know only after reading package metadata?
- Why should a generated lockfile be committed but not normally hand-edited?
- What happens when `pyproject.toml` changes but the lock has not yet changed?
- What is the difference between the uv cache and the installed environment?
- What does `?=` mean in a Make variable assignment?
- What does `unexport` change, and what does it leave unchanged?
- Why are line-level answers comments rather than arbitrary triple-quoted
  strings?
- Why did all TOML text appear white before a TOML grammar was installed?
- Which readability problems belong in the file, and which belong in editor
  configuration or the color theme?

## Understanding check

Ask the learner to narrate:

```text
subject says use Pydantic
    -> human adds Pydantic constraint to pyproject.toml
    -> uv reads Pydantic package metadata
    -> uv selects Pydantic and its dependencies
    -> uv records exact resolution in uv.lock
    -> uv sync installs that resolution into /tmp environment
    -> selected interpreter makes those packages importable
```

Then repeat the chain for the local `llm-sdk`, ensuring the learner mentions
its nested `pyproject.toml` and transitive model dependencies.

## Likely misconceptions

- `uv.lock` was not copied from the subject or manually designed package by
  package.
- A lower-bound constraint is not necessarily the installed version.
- A package imported by a dependency need not be repeated as a root direct
  dependency.
- `tool.uv.sources` does not by itself declare that the package is required;
  it tells uv where to obtain an already declared dependency.
- The uv cache and virtual environment are not the same storage.
- `make install` delegates to uv; Make does not resolve Python packages.
- `uv sync` may update a stale lock unless a frozen/check-only mode is used.
- A comment before code is not a function docstring; a docstring is the first
  string expression in a module, class, or function body.

## Successful session outcome

The learner can trace every top-level TOML dependency to its source, explain
how the SDK adds transitive dependencies, describe how uv generated the lock,
and distinguish resolution, caching, installation, interpreter selection, and
Make orchestration.
