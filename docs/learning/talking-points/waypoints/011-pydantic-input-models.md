# Talking Points 011: Pydantic Input Models

Companion waypoint:
[011 — Pydantic input models](../../waypoints/011-2026-11-13-pydantic-input-models.md)

## Agent preparation

Read:

- the companion waypoint;
- the [input-validation theme](../themes/input-validation/index.md);
- [`src/models.py`](../../../../src/models.py);
- [`tests/test_models.py`](../../../../tests/test_models.py);
- the [input/output contract](../../../requirements/input-output-contract.md);
- the [implementation rules](../../../requirements/implementation-rules.md).

Focus on the input boundary and Pydantic concepts. Do not begin JSON loading
or model integration during the discussion unless the learner explicitly
changes the session's purpose.

## Short recap

The first production package and three strict Pydantic models were created.
Tests prove that supplied data validates and representative malformed data is
rejected. Q-002 was resolved with initial support for `string`, `number`, and
`boolean` value definitions.

## Conversation order

1. Why validation belongs before model inference.
2. Python type aliases and `Literal`.
3. Pydantic `BaseModel`, fields, and nested models.
4. `ConfigDict(extra="forbid", strict=True)`, silent-data-loss prevention,
   and coercion prevention.
5. `Field(min_length=1)` and the limits of the current rule.
6. `model_validate()` success and `ValidationError` failure.
7. What each test proves and does not prove.
8. The supported-type decision and future extension rule.
9. Why JSON loading and CLI work remain separate next steps.

## Trace one supplied function

Ask the learner to trace this conceptual conversion:

```text
raw dictionary
    -> FunctionDefinition.model_validate(...)
    -> name: str
    -> description: str
    -> parameters: dict[str, ValueDefinition]
    -> each nested type checked against ParameterType
    -> returns: ValueDefinition
```

Then change one property at a time and predict whether validation succeeds:

- remove `description`;
- add an unexpected top-level key;
- replace `number` with `array`;
- replace `number` with `boolean`;
- make `name` an empty string.

## Discussion prompts

- What makes incoming JSON “untrusted” even when it is supplied with the
  project?
- What does a Pydantic model add beyond a type hint?
- Why does `Literal` help both runtime validation and static analysis?
- Why use one `ValueDefinition` for parameters and return values?
- What does nested validation mean here?
- Why reject extra keys instead of ignoring them?
- Does `min_length=1` reject whitespace-only strings?
- Why are arrays rejected rather than partially supported?
- Why do passing model tests not prove file loading works?
- Why should these tests avoid constructing Qwen?
- What does `cast` change at runtime?

## Understanding checks

The learner should be able to:

- distinguish a raw dictionary from a validated model instance;
- explain every annotation and Pydantic setting in `src/models.py`;
- predict the result of each current test case;
- explain why `string`, `number`, and `boolean` are the initial supported set;
- identify file loading, CLI parsing, and output models as unfinished layers;
- distinguish focused checks passing from repository-wide supplied-SDK
  findings.

## Likely misconceptions

- Type hints alone do not validate runtime JSON.
- `BaseModel` is not the language model; it is Pydantic's data-model base.
- `extra="forbid"` rejects unknown keys, while `strict=True` rejects values
  that would require type coercion. Neither makes every valid string
  meaningful.
- `min_length=1` does not currently strip whitespace.
- `Literal` is not an enumeration class, although it enforces a similar fixed
  set here.
- A test expecting `ValidationError` passes because failure was the intended
  behavior.
- `cast` informs Mypy and performs no runtime conversion.
- No model inference occurred in this waypoint.

## Successful session outcome

The learner can read the complete model file, explain the validation boundary,
trace nested validation, describe what the tests establish, and state why JSON
loading is the next implementation slice.

## Related learning

- [Input-validation theme](../themes/input-validation/index.md)
- [Waypoint discussions](index.md)
- [Project status](../../../project/status.md)
- [Python project tooling](../themes/python-tooling/index.md)

## Voice-session follow-up notes (2026-11-17)

These are review requests from the learner, not claims that the next implementation slice is complete.

### Revisit on the next learning pass

- Walk through the exact sequence: JSON text -> `json.loads()` or `json.load()` -> Python dictionaries/lists -> `PromptInput.model_validate()` or `FunctionDefinition.model_validate()` -> validated Pydantic class instances.
- Distinguish a Pydantic `BaseModel` subclass from the Qwen language model: `tests/test_models.py` exercises Pydantic validation and does **not** construct or run Qwen.
- Point to the precise call sites in `tests/test_models.py`, including `load_object_list()`, the `PromptInput.model_validate(item)` list comprehension, and `FunctionDefinition.model_validate(item)`.
- Explain why the class definitions contain no explicit `return`, constructor, or user-written methods: Pydantic supplies validation and initialization through `BaseModel`.
- Revisit the distinction between Python static annotations / `Literal`, Pydantic runtime validation, and the terminology of declarative schemas; use TypeScript / Zod comparisons where helpful.
- Clarify that input validation is not generalized sanitization and that `strict=True` and `extra="forbid"` have distinct purposes.

### Future implementation / observability request

The learner wants **visible step-by-step diagnostic output** while running the project to follow the movement and transformation of data. During the forthcoming loader and integration work, consider an opt-in verbose/debug mode showing file reading, parsed top-level structure, per-item validation, creation of validated objects, and later prompt construction, inference, and output handling. Keep ordinary output clean, avoid dumping large/sensitive payloads, and do not introduce noisy prints into Pydantic model declarations or tests by default. The exact CLI/debug interface has not yet been decided.
