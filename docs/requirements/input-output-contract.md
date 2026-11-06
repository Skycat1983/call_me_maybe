# Input and Output Contract

Status: Active  
Source: Call Me Maybe subject, version 1.7

## Command-line interface

Run the program as a Python module:

```bash
uv run python -m src \
  [--functions_definition <function_definition_file>] \
  [--input <input_file>] \
  [--output <output_file>]
```

With no arguments, the program reads from `data/input/` and writes to `data/output/`.

Example with explicit paths:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json
```

## Prompt input

The default prompt file is:

```text
data/input/function_calling_tests.json
```

It contains a JSON array whose objects have a `prompt` string:

```json
[
  {"prompt": "What is the sum of 2 and 3?"},
  {"prompt": "Greet john"},
  {"prompt": "Reverse the string 'hello'"}
]
```

## Function definitions

The default definition file is:

```text
data/input/functions_definition.json
```

It contains a JSON array. Every function definition includes:

- `name`: function name.
- `description`: natural-language purpose.
- `parameters`: parameter names and their JSON-compatible types.
- `returns`: return type.

Example:

```json
[
  {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {
      "a": {"type": "number"},
      "b": {"type": "number"}
    },
    "returns": {"type": "number"}
  }
]
```

Evaluation may replace both supplied input files. Do not assume the example function names, descriptions, arguments, prompts, or order.

## Output file

The default output path is:

```text
data/output/function_calls.json
```

It contains one object per input prompt:

```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  }
]
```

Every result object contains exactly:

| Key | Type | Meaning |
|---|---|---|
| `prompt` | string | Original natural-language request. |
| `name` | string | Selected function name. |
| `parameters` | object | Every required argument with its declared type. |

## Output validation

- The complete output file must be valid JSON.
- Comments and trailing commas are forbidden.
- Result objects may contain no keys other than `prompt`, `name`, and `parameters`.
- Explanatory prose is forbidden in the output.
- `name` must identify a supplied function.
- Every required parameter must be present.
- Parameter names and types must exactly match the selected definition.
- Every result must be parseable and schema-compliant.

## Input and runtime errors

The program must handle these conditions gracefully:

- Missing input or definition file.
- Invalid JSON.
- Incorrect top-level or field types.
- Missing required input fields.
- Empty input.
- Unsupported or malformed function definitions.
- File read or write failure.
- Ambiguous or difficult prompts.

Errors must be clear and must not cause an unexpected traceback or crash during ordinary use.

The subject does not define a required error-output JSON schema. Any implementation-specific behavior for per-prompt failures should therefore be documented as a design decision and tested.
