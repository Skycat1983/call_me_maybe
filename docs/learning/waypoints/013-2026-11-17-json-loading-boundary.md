# Waypoint 013: JSON Loading Boundary

- Date: 2026-11-17
- Stage: Application input boundary
- Status: Complete

Voice discussion:
[Talking points 013](../talking-points/waypoints/013-json-loading-boundary.md)

## Purpose

Turn paths containing untrusted JSON into validated prompt or function
definition models, while converting ordinary file, decoding, structure, and
item-validation failures into clear application errors.

## Boundary implemented

The complete input path is now:

```text
path
    -> open UTF-8 file
    -> parse JSON
    -> require a non-empty top-level array
    -> validate each item with Pydantic
    -> list of trusted application models
```

This waypoint does not choose default paths, parse command-line arguments,
load the LLM, or produce output records.

## Code created

### `src/loaders.py`

Two public functions express the application's input operations:

- `load_prompts(path)` returns `list[PromptInput]`;
- `load_function_definitions(path)` returns
  `list[FunctionDefinition]`.

Both call the private generic `_load_model_list()` helper. `ModelT` is a type
variable bounded by `BaseModel`, allowing the helper to return the same model
type it receives without duplicating file and JSON mechanics.

`InputLoadError` translates expected boundary failures into one application
exception. Exception chaining with `raise ... from error` preserves the
original `OSError`, `UnicodeError`, `JSONDecodeError`, or `ValidationError` for
debugging. Pydantic failures also report the zero-based JSON array index.

Empty arrays are rejected because an empty prompt workload or function
catalogue cannot produce the required results.

### `tests/test_loaders.py`

Nine focused tests prove:

- both supplied files return typed models;
- input order and nested validation are preserved;
- a missing file becomes `InputLoadError` with `FileNotFoundError` as cause;
- malformed JSON reports its line and column;
- invalid UTF-8 becomes a readable input error;
- a non-array top-level value is rejected;
- an empty array is rejected;
- an invalid prompt reports its array index;
- an invalid function definition uses the correct boundary label;
- Pydantic failures retain `ValidationError` as their cause.

Temporary malformed inputs use pytest's `tmp_path`, so tests do not add
fixtures to the repository or interfere with one another.

## Questions and answers

### Why have two public functions and one generic helper?

Callers get names and return types that express their intent, while the
repeated file, parsing, structure, and iteration logic has one implementation.
The helper remains private because callers do not need to choose arbitrary
model classes.

### Why validate items one at a time instead of validating the whole list?

Iteration makes the failing array index explicit and keeps the error message
connected to the source file. It also preserves the supplied order naturally.

### Why create `InputLoadError` instead of exposing every low-level exception?

The future CLI needs one expected application boundary that it can catch and
display cleanly. The chained cause retains the low-level detail for tests and
debugging without forcing CLI code to understand every library exception.

### Why is the index zero-based?

It matches Python list indexing and can be used directly while debugging the
parsed data. A future user-facing CLI may choose to add a human-oriented item
number while retaining this precise index internally.

### Why did `python -m pytest` repair the Make target?

In this environment, the `pytest` console-script entry did not make the local
`src` package importable during collection. Starting pytest as a module through
the selected interpreter puts the project directory on Python's import path.
The repaired target now passes the complete suite.

## Validation evidence

```text
python -m pytest tests/test_loaders.py  -> 9 passed
make test                               -> 22 passed
flake8 src/loaders.py tests/test_loaders.py
                                        -> no findings
mypy src/loaders.py tests/test_loaders.py
                                        -> no issues in 2 source files
py_compile src/loaders.py               -> passed
```

## Decisions

- Empty prompt and function-definition arrays are invalid.
- Public loaders accept both `str` and `Path` values.
- The loader does not own default paths or CLI behavior.
- File, decoding, structure, and Pydantic failures cross the boundary as
  `InputLoadError`.
- Original exceptions remain available through `__cause__`.
- The Make test target invokes `python -m pytest`.

## Documents created or updated

- [`src/loaders.py`](../../../src/loaders.py)
- [`tests/test_loaders.py`](../../../tests/test_loaders.py)
- [`Makefile`](../../../Makefile)
- [Input-validation theme](../talking-points/themes/input-validation/index.md)
- [Project tasks](../../project/tasks.md)
- [Project status](../../project/status.md)
- [Known issues](../../project/issues.md)

## Next step

Discuss the complete file-to-model flow, then add the CLI shell that chooses
default or explicit paths and catches `InputLoadError` without printing an
unexpected traceback.
