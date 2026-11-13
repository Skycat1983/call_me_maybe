# Waypoint 011: Pydantic Input Models

- Date: 2026-11-13
- Stage: Application input boundary
- Status: Complete

Voice discussion:
[Talking points 011](../talking-points/waypoints/011-pydantic-input-models.md)

## Purpose

Create the first production application code as a small, model-free slice:
represent prompt objects and function definitions as strict Pydantic models,
then prove their behavior with focused tests.

## Why this code came first

External JSON should not flow directly into prompt construction or model
generation. The intended boundary is:

```text
untrusted JSON
    -> Pydantic validation
    -> trusted application objects
    -> later prompt construction and constrained decoding
```

This layer can be understood and tested without loading Qwen. It establishes
clear input shapes before the expensive and more complex inference work.

## Code created

### `src/__init__.py`

Creates the application package. It does not yet provide the required module
entry point; `src/__main__.py` will be added with the CLI shell later.

### `src/models.py`

Defines:

- `ParameterType`, a type alias restricting declared value types;
- `PromptInput`, containing one non-empty `prompt` string;
- `ValueDefinition`, containing one supported JSON-compatible type;
- `FunctionDefinition`, containing `name`, `description`, `parameters`, and
  `returns`.

Every class inherits from Pydantic's `BaseModel`, as required by the subject.
Every model uses `ConfigDict(extra="forbid", strict=True)`, so unknown keys
produce a validation error and incorrect runtime types are not coerced into
the declared type.

`Field(min_length=1)` rejects empty prompt, name, and description strings. It
does not yet reject a string containing only whitespace; that policy can be
made explicit when the file-loading error behavior is designed.

### `tests/test_models.py`

The focused tests verify that:

- all 11 supplied prompt objects validate;
- all five supplied function definitions validate;
- a missing prompt fails;
- an empty prompt fails;
- extra prompt or function fields fail;
- non-string prompt text and non-mapping parameters fail;
- `string`, `number`, and `boolean` types validate;
- an unknown `array` type fails;
- a function definition missing its description fails.

The tests read the real demonstration JSON, but they test only model
validation. Production file loading has not yet been implemented.

## Q-002 resolved: supported parameter types

The initial supported set is:

```python
Literal["string", "number", "boolean"]
```

Evidence and reasoning:

- supplied definitions use `string` and `number`;
- the subject explicitly requires constrained JSON syntax to support
  booleans;
- evaluation may replace the demonstration definitions;
- arrays, nested objects, and null-valued parameters are not explicitly
  required by the current source material.

Unknown types are rejected clearly rather than accepted without a decoder
capable of enforcing them. If later authoritative requirements add a type,
the alias, decoder, and tests must be extended together.

## Pydantic concepts introduced

### Model versus ordinary dictionary

A dictionary can contain any keys and values. A Pydantic model describes an
expected shape, validates incoming data, and exposes typed attributes such as
`prompt.prompt` or `definition.parameters`.

### `Literal`

`Literal` limits a value to named constants. It provides both a static type
for Mypy and runtime validation through Pydantic.

### `Field`

`Field(min_length=1)` adds a validation constraint to a string field. The
Python annotation remains `str`; the field metadata adds the non-empty rule.

### `model_validate()`

`model_validate(raw_object)` asks Pydantic to turn untrusted dictionary data
into a validated model. It returns the model on success and raises
`ValidationError` on failure.

### Nested validation

`FunctionDefinition.parameters` is declared as
`dict[str, ValueDefinition]`. Pydantic therefore validates every nested
parameter object as a `ValueDefinition`, not merely the outer function object.

## Validation evidence

Focused validation passed:

```text
pytest tests/test_models.py  -> 13 passed
flake8 src tests             -> no findings
mypy src tests               -> no issues in 3 source files
py_compile                   -> passed
```

The repository-wide checks correctly distinguish new-code quality from
pre-existing supplied code:

- `flake8 .` still reports only the recorded supplied-SDK formatting issues;
- `mypy .` originally reported three supplied-SDK errors and one local probe
  `Any` return;
- the local probe return was repaired with `typing.cast`, without changing
  runtime behavior;
- the three supplied-SDK typing errors remain under issue I-002.

## Decisions and boundaries

- Model definitions belong in production `src/`, not in the learning
  experiment directory.
- Validation rejects unknown fields at every current model boundary.
- This waypoint does not implement file loading, CLI arguments, output
  records, model construction, function selection, or decoding.
- No SDK or Qwen process is required to test these classes.
- The local `cast` tells the type checker what `argparse` dynamically returns;
  it performs no runtime conversion or validation.

## Documents created or updated

- [`src/models.py`](../../../src/models.py)
- [`tests/test_models.py`](../../../tests/test_models.py)
- [Input-validation theme](../talking-points/themes/input-validation/index.md)
- [Project tasks](../../project/tasks.md)
- [Project status](../../project/status.md)
- [Open questions](../../project/questions.md)
- [Known issues](../../project/issues.md)

## Next step

Implement a focused JSON-loading layer that:

1. opens a supplied path with a context manager;
2. distinguishes missing/unreadable files from invalid JSON;
3. requires a top-level array;
4. validates every item with the appropriate Pydantic model;
5. converts low-level exceptions into clear application errors;
6. remains testable without loading the LLM.
