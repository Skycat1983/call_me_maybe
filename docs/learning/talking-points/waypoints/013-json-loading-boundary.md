# Talking Points 013: JSON Loading Boundary

Companion waypoint:
[013 — JSON loading boundary](../../waypoints/013-2026-11-17-json-loading-boundary.md)

## Files to have open

- [`src/loaders.py`](../../../../src/loaders.py) — the complete path from file access to typed model lists.
- [`tests/test_loaders.py`](../../../../tests/test_loaders.py) — the success and failure examples that specify loader behavior.
- [`src/models.py`](../../../../src/models.py) — the Pydantic model classes passed into the generic helper.
- [`Makefile`](../../../../Makefile) — the repaired `python -m pytest` test entry point.
- [Input/output contract](../../../requirements/input-output-contract.md) — the canonical file shapes and graceful-error requirement.
- [Input-validation theme](../themes/input-validation/index.md) — the living explanation connecting models, loading, tests, and future CLI work.

## Agent preparation

Open the files above. Focus on the boundary between untrusted external data
and trusted application objects. Let the learner trace each success and
failure path before explaining it. Do not begin the CLI or LLM integration
unless the learner explicitly changes the session's purpose.

## Short recap

The application can now load both supplied JSON files into typed Pydantic
objects. One private generic helper owns repeated mechanics; two public
functions communicate caller intent. Expected failures become
`InputLoadError`, and nine loader tests prove the boundary.

## Conversation order

1. Follow a valid prompt file from `Path` to `list[PromptInput]`.
2. Identify what `ModelT` means and why it is bounded by `BaseModel`.
3. Compare the two public wrappers with the private generic helper.
4. Trace file, Unicode, JSON, structure, empty-array, and item failures.
5. Explain exception translation and `raise ... from error`.
6. Read each test as a behavioral example.
7. Explain `tmp_path`, test isolation, and why fixtures are temporary.
8. Compare the pytest console script with `python -m pytest`.
9. State what remains outside this boundary.

## Success-path trace

Ask the learner to explain what each value holds:

```text
path argument
    -> input_path: Path
    -> input_file: opened UTF-8 text stream
    -> raw_data: object returned by json.load
    -> validated_items: list[ModelT]
    -> list[PromptInput] or list[FunctionDefinition]
```

Then locate where the runtime checks narrow `raw_data` from a general object
to a list and where Pydantic narrows each raw item to a trusted model.

## Failure-path trace

| Failure | Detected by | Public result |
|---|---|---|
| Missing or unreadable file | `Path.open()` | `InputLoadError` chained from `OSError` |
| Invalid UTF-8 | text decoding | `InputLoadError` chained from `UnicodeError` |
| Malformed JSON | `json.load()` | `InputLoadError` with line and column |
| Top level is not an array | `isinstance(raw_data, list)` | `InputLoadError` naming the actual type |
| Empty array | `if not raw_data` | `InputLoadError` requiring at least one item |
| Invalid item | `model_validate()` | `InputLoadError` with index and chained `ValidationError` |

## Discussion prompts

- What is untrusted at the start, and what is trusted at the end?
- Why is `raw_data` annotated as `object` rather than pretending it is a list?
- What does `TypeVar("ModelT", bound=BaseModel)` allow Mypy to preserve?
- Why are `load_prompts()` and `load_function_definitions()` not replaced by
  one public “load anything” function?
- Why does the structure check happen before item validation?
- What information would be lost without exception chaining?
- Why does an invalid item report an index?
- Which tests inspect error messages, and which inspect `__cause__`?
- Why does `tmp_path` make failure tests independent?
- What should the future CLI catch, and what should it avoid printing?

## Understanding checks

Ask the learner to predict:

- the type returned from each public loader;
- which branch handles a JSON object instead of an array;
- whether `[]` reaches Pydantic validation;
- the reported index when the second item is invalid;
- the difference between `InputLoadError` and its `__cause__`;
- whether the loader chooses default file paths;
- why `make test` now uses `python -m pytest`.

## Likely misconceptions

- Parsing valid JSON does not prove that its structure matches the project.
- A type annotation does not validate runtime data; Pydantic does that work.
- A generic private helper does not make the public API vague.
- Exception chaining is not the same as displaying a traceback to the user.
- `tmp_path` is supplied separately to each test and is not project data.
- The loader validates input files; it does not yet parse CLI arguments.

## Related thematic learning

- [Input validation and data models](../themes/input-validation/index.md)
- [Python project tooling](../themes/python-tooling/index.md)
- [Talking points 011 — Pydantic input models](011-pydantic-input-models.md)

## Successful session outcome

The learner can trace both public loaders through the generic helper, explain
where every failure is detected, connect each branch to a test, and state why
the returned objects are safer for later application logic than raw JSON data.
