# Talking Points 005: Environment Repair and Cache Placement

Companion waypoint:
[005 — Environment repair and cache placement](../waypoints/005-2026-11-10-environment-repair-and-cache-placement.md)

## Agent preparation

Read the companion waypoint and the root `Makefile`. Keep the discussion
focused on storage roles and reproducibility. Do not instantiate Qwen during
the voice session unless explicitly requested.

## Short recap

The environment was incomplete. Redirecting only the `uv` cache did not move
installed packages, so the local `.venv` filled the home filesystem. The
Makefile now places the environment, package cache, and future Hugging Face
cache under `/tmp`. The repaired environment imports successfully, and the
redundant `.venv` was removed.

## Key concepts to discuss

1. Project declaration: `pyproject.toml`.
2. Resolved dependency versions: `uv.lock`.
3. Installed packages: `UV_PROJECT_ENVIRONMENT`.
4. Re-downloadable package artifacts: `UV_CACHE_DIR`.
5. Model and tokenizer files: `HF_HOME`.
6. Incremental synchronization with `uv sync`.
7. Reproducible generated data versus unique source data.
8. Persistent home storage versus potentially temporary `/tmp` storage.

## Discussion prompts

- Why did setting `UV_CACHE_DIR` not stop `.venv` from growing?
- Which directory must Python use to import `transformers`?
- Where will Qwen weights go, and when will they be downloaded?
- What happens when `make install` is run a second time?
- Why was the replacement environment verified before deleting `.venv`?
- Which files allow the `/tmp` environment to be recreated?
- Why is `UV_LINK_MODE=copy` useful across filesystems?
- What is the tradeoff of putting reproducible data in `/tmp`?
- Why might a direct `uv run` behave differently from `make run`?

## Understanding check

Ask the learner to map each item:

| Item | Location or controller |
|---|---|
| Desired direct dependencies | `pyproject.toml` |
| Exact resolved package graph | `uv.lock` |
| Importable installed packages | `/tmp/call-me-maybe-venv` |
| Downloaded Python package artifacts | `/tmp/call-me-maybe-uv-cache` |
| Future Qwen/tokenizer cache | `/tmp/call-me-maybe-huggingface` |
| Project source | Git workspace |

Then ask which locations can be deleted and recreated and which must be
preserved in Git.

## Likely misconceptions

- A package cache is not the installed environment.
- `uv lock` does not install packages.
- `uv sync` does not download model weights.
- Importing the SDK does not construct the model.
- `HF_HOME` does not control Python package installation.
- Moving reproducible files to `/tmp` saves quota but may require recreation
  after a restart.
- A successful lock resolution does not prove the current environment is
  complete.

## Successful session outcome

The learner can explain all three storage layers, predict where a dependency
or model download will go, and explain why `make install` is safe to rerun.
