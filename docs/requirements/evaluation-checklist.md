# Evaluation Checklist

Status: Working checklist  
Source: Call Me Maybe subject, version 1.7

Use this before submission. The linked requirement documents are canonical; this file records completion.

## Core behavior

See [requirements overview](overview.md) and [constrained decoding](constrained-decoding.md).

- [ ] Natural-language prompts are converted into function calls.
- [ ] The LLM selects the function.
- [ ] No hardcoded prompt mappings or selection heuristics are used.
- [ ] Decoding is constrained token by token.
- [ ] Constraints enforce JSON syntax and the selected function schema.
- [ ] The solution works with `Qwen/Qwen3-0.6B`.
- [ ] Different prompts and function sets work without code changes.

## Input, output, and errors

See [input/output contract](input-output-contract.md).

- [ ] The required CLI and all optional path arguments work.
- [ ] Default input paths work.
- [ ] Default output path works.
- [ ] Prompt input is validated.
- [ ] Function definitions are validated.
- [ ] Missing files produce clear errors.
- [ ] Invalid JSON produces clear errors.
- [ ] Every result has exactly `prompt`, `name`, and `parameters`.
- [ ] Every required parameter is present.
- [ ] Parameter names and types match the selected definition.
- [ ] Output contains no prose, comments, or trailing commas.
- [ ] Every generated output file parses successfully.

## Quality and tooling

See [implementation rules](implementation-rules.md).

- [ ] Python 3.10 or later is used.
- [ ] `uv sync` installs the project.
- [ ] All project classes use Pydantic.
- [ ] Project code uses only permitted dependencies and public SDK methods.
- [ ] Functions and classes have type hints and PEP 257 docstrings.
- [ ] `flake8 .` passes.
- [ ] The mandatory `mypy` command passes.
- [ ] Errors and resources are handled safely.
- [ ] The Makefile provides `install`, `run`, `debug`, `clean`, and `lint`.
- [ ] `.gitignore` excludes Python artifacts and generated output.

## Performance and testing

- [ ] Function selection and argument extraction reach at least 90% accuracy.
- [ ] JSON and schema validity reach 100%.
- [ ] The full prompt set finishes in under five minutes on standard hardware.
- [ ] Tests cover empty strings.
- [ ] Tests cover large numbers.
- [ ] Tests cover special characters and JSON escaping.
- [ ] Tests cover malformed and missing input.
- [ ] Tests cover ambiguous prompts.
- [ ] Tests cover multiple parameters and types.
- [ ] Tests use function definitions beyond the supplied examples.

## README

- [ ] `README.md` is at the repository root and written in English.
- [ ] Its first line is italicized and credits the 42 curriculum and project authors.
- [ ] It contains Description, Instructions, and Resources sections.
- [ ] Resources describe where and how AI was used.
- [ ] It explains the constrained-decoding algorithm.
- [ ] It explains design decisions.
- [ ] It analyzes accuracy, speed, and reliability.
- [ ] It records challenges and their solutions.
- [ ] It explains the testing strategy.
- [ ] It includes runnable examples.

## Repository and submission

- [ ] `src/` contains the implementation.
- [ ] `data/input/` contains demonstration files.
- [ ] `llm_sdk/` contains the supplied SDK.
- [ ] Root `pyproject.toml` and `uv.lock` are present.
- [ ] Root `Makefile` is present.
- [ ] Root `README.md` is complete.
- [ ] `data/output/` is not committed.
- [ ] Filenames and paths have been checked.
- [ ] All required work is committed and pushed.
- [ ] The implementation can be explained and modified during evaluation.

## Bonus readiness

Review bonus work only after every mandatory item passes.

- [ ] Any claimed bonus is implemented and demonstrable.
- [ ] Additional model support does not break the required model.
- [ ] Any custom tokenizer implementation integrates with constrained decoding.
- [ ] Additional libraries used for bonus work can be justified.
