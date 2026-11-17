# Theme: Input Validation and Data Models

- Kind: Thematic talking-point index
- Status: Living
- Last reviewed: 2026-11-17
- Prerequisites: Basic Python classes, dictionaries, and type hints

## Files to have open

- [`src/models.py`](../../../../../src/models.py) — the Pydantic models and validation rules discussed in this theme.
- [`src/loaders.py`](../../../../../src/loaders.py) — the file, JSON, array, and per-item validation boundary.
- [`src/cli.py`](../../../../../src/cli.py) — the path selection and expected-error presentation layer above the loaders.
- [`tests/test_models.py`](../../../../../tests/test_models.py) — the examples that prove accepted and rejected inputs.
- [`tests/test_loaders.py`](../../../../../tests/test_loaders.py) — the loader's success cases, failure branches, messages, and chained causes.
- [`tests/test_cli.py`](../../../../../tests/test_cli.py) — the tests proving CLI paths and loader errors cross the process boundary correctly.
- [`data/input/functions_definition.json`](../../../../../data/input/functions_definition.json) — supplied nested data exercised by the models.
- [`data/input/function_calling_tests.json`](../../../../../data/input/function_calling_tests.json) — the supplied prompt shape at the other input boundary.
- [Input/output contract](../../../../requirements/input-output-contract.md) — the canonical requirements against which the models are judged.

## Purpose

Use this theme to understand how external JSON becomes trusted application
data. It currently covers the Pydantic model and JSON-loading layers and will
also shows how the CLI selects their paths and presents expected failures. It
will expand when output models and output validation are implemented.

## Five-minute mental model

```text
CLI-selected path
    -> JSON text on disk
    -> file and JSON loader
    -> raw Python list/dictionaries
    -> Pydantic model_validate()
    -> PromptInput and FunctionDefinition objects
    -> later application and model logic
```

The model and loader steps now exist and have separate focused tests. Neither
layer depends on command-line parsing or the LLM.

## Current models

| Model or alias | Responsibility |
|---|---|
| `ParameterType` | Permit `string`, `number`, or `boolean` declarations |
| `PromptInput` | Require one non-empty natural-language `prompt` |
| `ValueDefinition` | Validate the declared type of one parameter or return value |
| `FunctionDefinition` | Validate a function's name, description, parameters, and return definition |

Canonical source: [`src/models.py`](../../../../../src/models.py).

## Read the code from top to bottom

### Module docstring and imports

The module docstring states its responsibility. `Literal` describes a closed
set of allowed values. Pydantic supplies the model base, configuration, and
field constraint.

### `ParameterType`

```python
ParameterType = Literal["string", "number", "boolean"]
```

This is a type alias, not a new runtime class. Pydantic reads the annotation
and rejects other strings during model validation.

The initial set resolves Q-002. It covers the supplied `string` and `number`
definitions plus JSON booleans explicitly required by the subject. Unsupported
types fail early instead of reaching a decoder that cannot enforce them.

### `PromptInput`

The `prompt` annotation says the validated attribute is a string.
`Field(min_length=1)` rejects `""`. `extra="forbid"` rejects keys outside the
model, and `strict=True` prevents another runtime type from being coerced into
a string. A whitespace-only string is not yet rejected because this model does
not strip whitespace.

### `ValueDefinition`

This model mirrors objects such as `{"type": "number"}`. Reusing it for both
parameter definitions and return definitions avoids two classes with identical
behavior.

### `FunctionDefinition`

The `parameters` annotation is important:

```python
dict[str, ValueDefinition]
```

Keys are parameter names. Each value must itself validate as a
`ValueDefinition`. That recursive behavior is nested validation.

## Current loading boundary

Canonical source: [`src/loaders.py`](../../../../../src/loaders.py).

The public functions describe the two operations needed by the application:

- `load_prompts(path)` returns `list[PromptInput]`;
- `load_function_definitions(path)` returns
  `list[FunctionDefinition]`.

Both delegate repeated mechanics to the private generic helper
`_load_model_list()`. The helper reads UTF-8 JSON, requires a non-empty
top-level array, validates every item with the requested Pydantic model, and
preserves input order.

`InputLoadError` is the application-level failure boundary. Its message
identifies the failed stage, while exception chaining preserves the original
file, decoding, or Pydantic exception as `__cause__` for debugging. Per-item
validation errors include the zero-based array index. The future CLI will
decide how to display these errors without a traceback.

These are current design decisions:

- empty prompt and function-definition arrays are rejected;
- public functions remain specific and readable;
- shared mechanics live in one private generic helper;
- the loader accepts `str` and `Path` inputs;
- loading does not choose default paths or parse command-line arguments.

## CLI handoff

The loader remains independent of command-line concerns. `src/cli.py` chooses
default or explicit paths, passes the two input paths into the public loaders,
and catches only `InputLoadError`.

An expected loader failure becomes one concise `stderr` message and exit code
`1`. Argparse separately owns invalid command syntax and exit code `2`.
Unexpected exceptions remain visible. The complete CLI concepts and evidence
live in the [command-line interface theme](../command-line-interface/index.md).

## Why forbid extra fields?

Silently ignoring a misspelled or unexpected field can make invalid input look
valid. For example, `"descripton"` should not disappear while the program
continues. Strict boundaries produce an early, local error that can later be
reported with the filename and item position.

`extra="forbid"` controls unknown keys. `strict=True` controls type coercion.
Neither automatically enforces semantic policies such as unique function names
or non-whitespace text.

## What the tests prove

[`tests/test_models.py`](../../../../../tests/test_models.py) proves:

- the demonstration objects match the current models;
- required fields, minimum lengths, and strict runtime types are active;
- unknown fields are rejected;
- nested function value definitions validate;
- the three supported type names pass;
- an unsupported type fails with `ValidationError`.

[`tests/test_loaders.py`](../../../../../tests/test_loaders.py) proves:

- both supplied files become typed model lists;
- missing files and invalid UTF-8 become readable input errors;
- malformed JSON reports a line and column;
- non-array and empty top-level values are rejected;
- invalid items report their array index and boundary label;
- low-level file, JSON, Unicode, and Pydantic failures remain available as
  chained causes where applicable.

The tests do not yet prove:

- generated output matches a selected function;
- any LLM behavior.

## Focused versus repository-wide checks

The production models and tests pass focused pytest, Flake8, Mypy, and compile
checks. Repository-wide Flake8 and Mypy still find issues in the supplied SDK,
tracked as I-002. A validation report should keep those two facts separate.

## Voice-session routes

Choose one route:

- **Overview:** explain the five-minute mental model and current model table.
- **Code:** read `src/models.py` line by line and predict each field's runtime
  behavior.
- **Tests:** predict success, `ValidationError`, or `InputLoadError` before
  reading each model or loader test.
- **Loader flow:** trace `Path` through JSON parsing, list checks, item
  validation, and the typed return value.
- **Theory:** compare static type hints, runtime validation, and trusted
  application objects.
- **Design boundaries:** identify policies not yet represented by these
  models.

Ask the agent to let the learner predict first, then run or inspect evidence.

## Questions to revisit as the theme grows

- Should whitespace-only prompts, names, or descriptions be rejected?
- Where should duplicate function names be detected?
- How should an unsupported declared type be reported to the CLI user?
- How will generated parameter values be checked against the selected
  `FunctionDefinition`?

## Related learning

- [Talking-points hub](../../index.md)
- [Thematic discussions](../index.md)
- [Waypoint 011 discussion](../../waypoints/011-pydantic-input-models.md)
- [Waypoint 011 record](../../../waypoints/011-2026-11-13-pydantic-input-models.md)
- [Waypoint 013 discussion](../../waypoints/013-json-loading-boundary.md)
- [Waypoint 013 record](../../../waypoints/013-2026-11-17-json-loading-boundary.md)
- [Waypoint 014 discussion](../../waypoints/014-cli-input-shell.md)
- [Waypoint 014 record](../../../waypoints/014-2026-11-17-cli-input-shell.md)
- [Input/output contract](../../../../requirements/input-output-contract.md)
- [Implementation rules](../../../../requirements/implementation-rules.md)
- [Project status](../../../../project/status.md)
- [Python project tooling](../python-tooling/index.md)
- [Command-line interface](../command-line-interface/index.md)
