# Python Import Resolution in the SDK

Status: Learning reference  
Source: `llm_sdk/llm_sdk/__init__.py`

Learning context: [Waypoint 004](../learning/waypoints/004-2026-11-10-supplied-data-and-llm-sdk.md)

## Imports used by the SDK

### PyTorch

```python
import torch
```

PyTorch provides:

- Tensor storage and operations.
- Integer and floating-point dtypes.
- CPU, CUDA, and MPS device detection.
- `torch.no_grad()` for inference without gradient tracking.

### Hugging Face Hub

```python
from huggingface_hub import hf_hub_download
```

`hf_hub_download` retrieves individual model or tokenizer files and returns
their local cache paths.

### Transformers

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    logging,
)
```

- `AutoTokenizer` selects the correct tokenizer class for a model repository.
- `AutoModelForCausalLM` selects a model that predicts the next token.
- `PreTrainedTokenizer` and `PreTrainedModel` are type annotations for the
  stored tokenizer and model.
- `logging` controls Transformers' console output.

The original SDK also imported `os`, `time`, and `Tuple`, but did not use
them. Unused imports add noise and fail Flake8's `F401` check, so they were
removed rather than treated as dependencies.

## How Python resolves an import

For an import such as:

```python
import torch
```

Python searches locations listed in `sys.path`. These generally include:

1. The running script or current project location.
2. Python's standard-library directories.
3. The active environment's `site-packages`.
4. Any explicitly configured additional paths.

`uv run` selects the project's virtual environment, so third-party imports are
resolved from `.venv` after `uv sync` installs them.

The local SDK is declared in the root `pyproject.toml`:

```toml
[project]
dependencies = ["llm-sdk", "..."]

[tool.uv.sources]
llm-sdk = { path = "llm_sdk" }
```

This tells `uv` that the `llm-sdk` dependency comes from the repository's
`llm_sdk/` directory rather than the public package index. That package then
declares PyTorch, Transformers, and Hugging Face Hub as its own dependencies.

## Python packages are not model weights

Resolving:

```python
from transformers import AutoTokenizer
```

loads Python code from the virtual environment.

Calling:

```python
AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")
```

is different: it requests model-specific files from Hugging Face and caches
them locally. Package installation and model download therefore happen at
different times.

## Editor “go to definition”

An editor can navigate into imported code only when its Python language server
uses the correct interpreter. For this project, select:

```text
<project>/.venv/bin/python
```

Once dependencies are completely installed and the editor has indexed that
environment, “go to definition” should open library source or type
information. If it cannot resolve an import, first verify:

1. The selected interpreter.
2. That `uv sync` completed.
3. That the package appears in `uv pip list`.
4. That an import-only command succeeds.
