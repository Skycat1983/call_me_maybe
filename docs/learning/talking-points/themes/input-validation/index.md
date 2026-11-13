# Theme: Input Validation and Data Models

- Kind: Thematic talking-point index
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: Basic Python classes, dictionaries, and type hints

## Purpose

Use this theme to understand how external JSON becomes trusted application
data. It currently covers the Pydantic model layer and will expand when file
loading, CLI path handling, application errors, and output validation are
implemented.

## Five-minute mental model

```text
JSON text on disk
    -> future file and JSON loader
    -> raw Python list/dictionaries
    -> Pydantic model_validate()
    -> PromptInput and FunctionDefinition objects
    -> later application and model logic
```

Only the Pydantic step exists now. The tests deliberately call it directly so
model behavior is proven independently of files, command-line parsing, or the
LLM.

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

The tests do not yet prove:

- files are opened safely;
- invalid JSON gets a clear application message;
- the top-level value must be an array;
- item errors include useful locations;
- CLI default or explicit paths work;
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
- **Tests:** predict success or `ValidationError` before reading each test.
- **Theory:** compare static type hints, runtime validation, and trusted
  application objects.
- **Design boundaries:** identify policies not yet represented by these
  models.

Ask the agent to let the learner predict first, then run or inspect evidence.

## Questions to revisit as the theme grows

- Should whitespace-only prompts, names, or descriptions be rejected?
- Where should duplicate function names be detected?
- How should an unsupported declared type be reported to the CLI user?
- Should file loaders be generic or separate for prompts and definitions?
- Which application exception types give clear messages without exposing
  tracebacks?
- How will generated parameter values be checked against the selected
  `FunctionDefinition`?

## Related learning

- [Talking-points hub](../../index.md)
- [Thematic discussions](../index.md)
- [Waypoint 011 discussion](../../waypoints/011-pydantic-input-models.md)
- [Waypoint 011 record](../../../waypoints/011-2026-11-13-pydantic-input-models.md)
- [Input/output contract](../../../../requirements/input-output-contract.md)
- [Implementation rules](../../../../requirements/implementation-rules.md)
- [Project status](../../../../project/status.md)
- [Python project tooling](../python-tooling/index.md)
