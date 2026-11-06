# Implementation Rules

Status: Active  
Source: Call Me Maybe subject, version 1.7

## Runtime and dependency management

- Use Python 3.10 or later.
- Use `uv` for the virtual environment and dependency management.
- The evaluator and Moulinette will run `uv sync`.
- Include `numpy` and `pydantic`.
- Use Pydantic for every project class.
- Use the supplied `llm_sdk` package.
- Support `Qwen/Qwen3-0.6B`; it is the default required model.
- Additional models may be supported only if the required model continues to work.

## Prohibited implementation choices

Project code must not:

- Use DSPy or similar packages.
- Directly use PyTorch, Hugging Face packages, Transformers, or Outlines.
- Access private methods or attributes from `llm_sdk`.
- Replace LLM function selection with heuristics or hardcoded examples.

The supplied SDK may use otherwise prohibited packages internally; project code must interact with it only through its public interface.

## Code quality

- Follow `flake8`.
- Add type hints to parameters, return values, and variables where applicable.
- Pass `mypy` without errors.
- Add PEP 257 docstrings to functions and classes. Google or NumPy style is acceptable.
- Prefer context managers for files, connections, and similar resources.
- Release resources correctly.
- Handle exceptions gracefully.
- Return clear, useful error messages.
- Do not allow malformed inputs or normal edge cases to cause an unexpected crash.
- Include a `.gitignore` for Python artifacts.
- Develop inside an isolated virtual environment.

An unhandled exception during review may cause the project to be considered non-functional.

## Static checks

The mandatory lint commands are:

```bash
flake8 .
mypy . \
  --warn-return-any \
  --warn-unused-ignores \
  --ignore-missing-imports \
  --disallow-untyped-defs \
  --check-untyped-defs
```

An optional strict check may run:

```bash
flake8 .
mypy . --strict
```

## Makefile

The root `Makefile` must define:

| Target | Required behavior |
|---|---|
| `install` | Install project dependencies. |
| `run` | Run the main program. |
| `debug` | Run the main program with Python's debugger, such as `pdb`. |
| `clean` | Remove caches and temporary files such as `__pycache__` and `.mypy_cache`. |
| `lint` | Run the mandatory `flake8` and `mypy` commands. |
| `lint-strict` | Optional strict linting with `mypy --strict`. |

## Required repository contents

The submitted repository must contain:

```text
src/                 implementation
data/input/          demonstration input files
llm_sdk/             supplied SDK package
pyproject.toml       project dependencies and configuration
uv.lock              locked dependencies
Makefile             required task automation
README.md            required project documentation
```

Do not commit `data/output/`; it must be created when the program runs.

Only committed repository content is evaluated. Check names and locations before submission.

## Development tests

Development tests are strongly recommended and may use `pytest` or `unittest`. The subject describes them as non-submitted and non-graded, although a comprehensive test suite may qualify as bonus work.
