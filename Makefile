# Keep the environment and re-downloadable caches off the small home partition.
# Callers can override any path, for example: make UV_CACHE_DIR=/other install
# `?=` means "use this default only if the caller did not provide another one."
UV_PROJECT_ENVIRONMENT ?= /tmp/call-me-maybe-venv
# ? what is the cache used for?
# Answer: uv keeps downloaded wheels, source archives, package metadata, and
# extracted package data here so later installs do not need to fetch or build
# everything again. It is disposable and is not the installed environment.
# ? what are wheels?
UV_CACHE_DIR ?= /tmp/call-me-maybe-uv-cache
# ? how do we know this should go there?
# Answer: Hugging Face libraries recognise the `HF_HOME` environment variable.
# We chose a /tmp path because model and tokenizer files are large,
# re-downloadable, and the /tmp filesystem has much more available space.
HF_HOME ?= /tmp/call-me-maybe-huggingface
# ? what is the relevance of this?
# Answer: uv can install files by copying, hard-linking, cloning, or symlinking
# them from its cache. `copy` gives the environment independent files, so
# clearing the uv cache does not leave installed packages pointing at it.
UV_LINK_MODE ?= copy

# `export` passes these Make variables to recipe processes such as uv and
# Python. That is how uv and Hugging Face see the selected storage locations.
export UV_PROJECT_ENVIRONMENT
export UV_CACHE_DIR
export HF_HOME
export UV_LINK_MODE

# An already activated environment must not override this project's location.
# ? how does unexport work?
# Answer: GNU Make removes VIRTUAL_ENV from the environment it gives to recipe
# processes. It does not deactivate or change the caller's shell. This prevents
# an unrelated activated environment from influencing project commands or
# producing environment-mismatch warnings.
unexport VIRTUAL_ENV

.PHONY: install run debug clean lint lint-strict test inspect-sdk \
	inspect-sdk-cpu

# ? what does sync do?
# Answer: `uv sync` reads pyproject.toml and uv.lock, creates the configured
# environment if necessary, and makes its installed packages match the locked
# dependency graph. If project requirements changed, uv normally resolves them
# and updates uv.lock before synchronising the environment.
install:
	uv sync

run:
	uv run python -m src

debug:
	uv run python -m pdb -m src

clean:
	find . -path './.git' -prune -o -path './.venv' -prune -o \
		-type d \( -name '__pycache__' -o -name '.mypy_cache' \
		-o -name '.pytest_cache' -o -name '.ruff_cache' \) \
		-prune -exec rm -rf {} +

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

test:
	uv run pytest

inspect-sdk:
	uv run python experiments/inspect_sdk.py

inspect-sdk-cpu:
	uv run python experiments/inspect_sdk.py --device cpu
