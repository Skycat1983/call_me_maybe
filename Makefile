# Keep the environment and re-downloadable caches off the small home partition.
# Callers can override any path, for example: make UV_CACHE_DIR=/other install
UV_PROJECT_ENVIRONMENT ?= /tmp/call-me-maybe-venv
UV_CACHE_DIR ?= /tmp/call-me-maybe-uv-cache
HF_HOME ?= /tmp/call-me-maybe-huggingface
UV_LINK_MODE ?= copy

export UV_PROJECT_ENVIRONMENT
export UV_CACHE_DIR
export HF_HOME
export UV_LINK_MODE

# An already activated environment must not override this project's location.
unexport VIRTUAL_ENV

.PHONY: install run debug clean lint lint-strict test inspect-sdk \
	inspect-sdk-cpu

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
