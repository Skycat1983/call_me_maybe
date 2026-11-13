# Waypoint 005: Environment Repair and Cache Placement

- Date: 2026-11-10
- Stage: Development environment
- Status: Complete

Voice discussion: [Talking points 005](../talking-points/waypoints/005-environment-and-cache-placement.md)

## Purpose

Repair the incomplete Python environment and keep large installed dependencies,
package downloads, and future model files off the constrained home filesystem.

## Topics covered

- The difference between an installed environment and a package download
  cache.
- The difference between Python packages and model files.
- `uv sync` as an incremental environment repair.
- `UV_PROJECT_ENVIRONMENT`, `UV_CACHE_DIR`, and `HF_HOME`.
- Why redirecting only a cache does not move installed packages.
- Verifying an environment before deleting a broken copy.

## Questions and answers

### Would rerunning `make install` install dependencies elsewhere?

Not with the original Makefile. `make install` ran `uv sync`, which repaired
the project environment at `.venv`. Redirecting `UV_CACHE_DIR` moved downloaded
archives and build artifacts, but the installed packages still went into
`.venv`.

To place installed packages elsewhere, `uv` also needs:

```text
UV_PROJECT_ENVIRONMENT=/tmp/call-me-maybe-venv
```

The Makefile now exports this value for all of its recipes.

### What does `UV_CACHE_DIR` control?

It controls re-downloadable package artifacts used by `uv`: wheels, source
archives, and build/cache data. It does not choose the installation location.

This project uses:

```text
/tmp/call-me-maybe-uv-cache
```

### What does `UV_PROJECT_ENVIRONMENT` control?

It tells `uv` where to create and use the installed Python environment. That
environment contains importable packages and console tools.

This project uses:

```text
/tmp/call-me-maybe-venv
```

### What does `HF_HOME` control?

It tells Hugging Face libraries where to cache downloaded model and tokenizer
files. These files are separate from the Python environment.

This project uses:

```text
/tmp/call-me-maybe-huggingface
```

No Qwen files were downloaded during this waypoint. The directory matters
when `Small_LLM_Model()` or a tokenizer-path method is deliberately called.

### Is rerunning `make install` wasteful?

No. `uv sync` is incremental. It compares the lockfile with the configured
environment and installs, removes, or updates only what is necessary.

After the repair, another `make install` reported:

```text
Resolved 102 packages
Checked 72 packages
```

It did not reinstall the complete environment.

### Why did the first repair attempt fill the home partition?

The package cache was correctly redirected to `/tmp`, but installation still
targeted `.venv` under the home-mounted workspace. The CUDA-enabled PyTorch
dependency set is large, so `.venv` grew to approximately 1.4 GB and home usage
returned to 95%.

### Why was the old `.venv` removed?

The replacement environment in `/tmp` was completed and successfully verified
first. The local `.venv` was incomplete, redundant, generated from the
lockfile, and consuming 1.4 GB. Removing it restored home space without
removing source code or unique data.

## Evidence and experiments

### Initial repair attempt

- `transformers` appeared in `.venv`.
- Import still failed because the installation had ended in an incomplete
  state.
- Home usage reached 95%.

### Relocated environment

`make install` created `/tmp/call-me-maybe-venv` and installed 72 packages.

An import-only verification produced:

```text
environment: /tmp/call-me-maybe-venv
llm_sdk:     /tmp/call-me-maybe-venv/lib/python3.10/site-packages/llm_sdk/__init__.py
transformers version: 5.20.2
```

This test imported the SDK without constructing `Small_LLM_Model`, so it did
not download Qwen.

### Storage after cleanup

```text
home size:      4.7 GB
home used:      3.1 GB
home available: 1.7 GB
home usage:     66%
```

The `/tmp` filesystem had approximately 226 GB available.

## Decisions

- Store the project environment under `/tmp` on this machine.
- Store the `uv` package cache under `/tmp`.
- Store future Hugging Face model/tokenizer files under `/tmp`.
- Export these locations from the Makefile so `install`, `run`, `debug`,
  `lint`, and `test` use the same environment.
- Use `?=` in the Makefile so callers can override any location.
- Set `UV_LINK_MODE=copy` because the cache and environment may be on
  different filesystems where hardlinks are unavailable.
- Remove `VIRTUAL_ENV` from Make recipes so a previously activated environment
  does not override or confuse the configured project environment.

## Operational consequence

`/tmp` is not guaranteed to survive a restart or system cleanup. If the
environment disappears, run:

```bash
make install
```

It will be recreated from `pyproject.toml` and `uv.lock`. Model files may also
need to be downloaded again if the Hugging Face cache is cleared.

Direct `uv` commands outside the Makefile do not automatically receive these
Makefile variables. Prefer the Make targets, or export the same variables in
the shell before running `uv` directly.

## Open questions or issues

- No model behavior was tested.
- Encode/decode and tokenizer-file questions remain open.
- The supplied SDK still has pre-existing Flake8 issues (`I-002`).

Issue `I-001`, the incomplete environment, is resolved by this waypoint.

## Documents created or updated

- `Makefile`
- `docs/reference/imports.md`
- `docs/reference/llm-sdk.md`
- `docs/project/issues.md`
- `docs/project/status.md`
- `docs/project/tasks.md`
- `docs/learning/index.md`
- `docs/learning/talking-points/index.md`

## Next step

Run the first intentional SDK behavior experiments: model construction,
encode/decode, tokenizer-file inspection, and one next-token logits call.
