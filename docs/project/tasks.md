# Project Tasks

Last reviewed: 2026-11-06

Tasks are grouped by milestone. Check an item only after its result has been verified.

## M0: Repository and requirements

- [x] Initialize the local Git repository.
- [x] Connect and push to the GitHub repository.
- [x] Extract the supplied archives.
- [x] Keep the PDF and ZIP archives local-only.
- [x] Extract the project subject into Markdown.
- [x] Preserve the condensed subject in the documentation archive.
- [x] Create focused requirement documents.
- [x] Create the documentation index.
- [x] Create the project status and task dashboards.

## M1: Supplied materials and project foundation

- [ ] Document the public `llm_sdk` interface and observable behavior.
- [ ] Inspect the supplied prompts and function definitions.
- [ ] Identify ambiguities that need decisions or experiments.
- [ ] Define component boundaries and data flow.
- [x] Decide the root package and configuration layout.
- [x] Create root `pyproject.toml` and `uv.lock`.
- [ ] Create the `src` package and module entry point.
- [x] Create the required Makefile.
- [x] Extend `.gitignore` for generated output and development caches.

## M2: Input, models, and CLI

- [ ] Define Pydantic models for prompts.
- [ ] Define Pydantic models for function definitions.
- [ ] Define Pydantic models for output records.
- [ ] Implement JSON file loading and validation.
- [ ] Implement CLI path arguments and defaults.
- [ ] Implement clear file and validation errors.
- [ ] Add focused tests for input and CLI behavior.

## M3: LLM integration and function selection

- [ ] Load the required model through the public SDK.
- [ ] Build the model prompt from a request and available definitions.
- [ ] Retrieve and interpret next-token logits.
- [ ] Verify that function selection comes from model scores.
- [ ] Test function selection with definitions not supplied in the examples.

## M4: Constrained decoding

- [ ] Load and interpret the model vocabulary.
- [ ] Define the partial-output state representation.
- [ ] Restrict function-name generation.
- [ ] Restrict parameter-name generation.
- [ ] Restrict string values and escapes.
- [ ] Restrict number values.
- [ ] Restrict boolean and other required values.
- [ ] Enforce delimiters, ordering rules, and completion.
- [ ] Prevent invalid tokens from being selected.
- [ ] Test tokens that contain multiple characters or structural fragments.

## M5: Output and reliability

- [ ] Generate one result per prompt.
- [ ] Validate every completed result against the chosen definition.
- [ ] Write the required JSON array.
- [ ] Ensure `data/output/` is generated but not committed.
- [ ] Test malformed files, empty input, special characters, and large numbers.
- [ ] Measure function-selection and argument-extraction accuracy.
- [ ] Confirm 100% JSON and schema validity.
- [ ] Confirm the full workload finishes within five minutes.

## M6: Quality and submission

- [ ] Pass `flake8`.
- [ ] Pass the mandatory `mypy` command.
- [ ] Verify type hints and docstrings.
- [ ] Verify graceful error handling.
- [ ] Complete the required README sections.
- [ ] Document architecture, algorithm, decisions, testing, and performance.
- [ ] Run every item in the evaluation checklist.
- [ ] Confirm required files are committed and generated output is absent.
- [ ] Push the reviewed final state.
