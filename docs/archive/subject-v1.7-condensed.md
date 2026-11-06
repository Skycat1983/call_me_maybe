# Call Me Maybe: Project Specification

Condensed from the project subject, version 1.7. This document preserves the implementation, validation, documentation, and submission requirements while omitting introductory and repetitive prose.

## Objective

Build a function-calling tool that converts natural-language prompts into structured function calls.

For example, given:

```text
What is the sum of 40 and 2?
```

the program must produce a function name and typed arguments, not calculate and return `42`:

```json
{
  "name": "fn_add_numbers",
  "parameters": {
    "a": 40.0,
    "b": 2.0
  }
}
```

The function must be selected by the LLM. Heuristics or hardcoded prompt-to-function mappings are forbidden.

The central requirement is constrained decoding: generated output must be restricted token by token so it is always valid JSON and conforms to the selected function's schema. Prompting the model to produce JSON without enforcing constraints is insufficient.

## Required environment and dependencies

- Python 3.10 or later.
- Use `uv` for the virtual environment and dependency management.
- The evaluator and Moulinette will run `uv sync`.
- Required packages include `numpy` and `pydantic`.
- All classes must use Pydantic for validation.
- Use the supplied `llm_sdk` package. It may be copied beside the `src` directory.
- The default required model is `Qwen/Qwen3-0.6B`.
- Other models may also be supported, but the project must work with `Qwen/Qwen3-0.6B`.

The project implementation must not use DSPy or similar packages, including direct use of PyTorch, Hugging Face packages, Transformers, or Outlines. Do not use private methods or attributes from `llm_sdk`.

## Code quality requirements

- Follow the `flake8` coding standard.
- Add type hints to function parameters, return types, and variables where applicable.
- Pass `mypy` without errors.
- Add PEP 257 docstrings to functions and classes. Google or NumPy style is acceptable.
- Handle errors gracefully and provide clear messages.
- Do not crash unexpectedly during review; an unhandled exception makes the project non-functional.
- Manage resources correctly. Prefer context managers for files, connections, and similar resources.
- Include a `.gitignore` for Python artifacts.
- Use a virtual environment.
- Tests are recommended for development but are not submitted or graded as part of the mandatory requirements.

## Required command-line interface

The program must run as a module:

```bash
uv run python -m src \
  [--functions_definition <function_definition_file>] \
  [--input <input_file>] \
  [--output <output_file>]
```

With no arguments, it must read from `data/input/` and write to `data/output/`.

Example with explicit paths:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json
```

## Input files

The default input directory is `data/input/` and contains two JSON files.

### `function_calling_tests.json`

A JSON array of objects containing natural-language prompts:

```json
[
  {"prompt": "What is the sum of 2 and 3?"},
  {"prompt": "What is the sum of 265 and 345?"},
  {"prompt": "Greet shrek"},
  {"prompt": "Greet john"},
  {"prompt": "Reverse the string 'hello'"}
]
```

### `functions_definition.json`

A JSON array describing the functions available to the model. Each definition contains:

- Function name.
- Description.
- Parameter names and types.
- Return type.

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
  },
  {
    "name": "fn_greet",
    "description": "Generate a greeting message for a person by name.",
    "parameters": {
      "name": {"type": "string"}
    },
    "returns": {"type": "string"}
  },
  {
    "name": "fn_reverse_string",
    "description": "Reverse a string and return the reversed result.",
    "parameters": {
      "s": {"type": "string"}
    },
    "returns": {"type": "string"}
  }
]
```

Input files may be missing or contain invalid JSON. These cases must produce clear errors without an unexpected crash.

Evaluation will use different prompts and function sets. Do not hardcode the supplied examples.

## LLM SDK interface

The supplied `Small_LLM_Model` wrapper exposes the allowed model interface.

### Required or available methods

```python
get_logits_from_input_ids(input_ids: list[int]) -> list[float]
```

Returns the model's logits for the supplied token IDs.

```python
get_path_to_vocab_file() -> str
```

Returns the path to the vocabulary file that maps token IDs to token strings.

```python
encode(text: str) -> Tensor
```

Encodes text as token IDs.

```python
decode(token_ids: list[int]) -> str
```

Optionally decodes token IDs to text.

Only public SDK methods and attributes may be used.

## Generation pipeline

Generation is iterative:

1. Start with the natural-language prompt and any required context.
2. Tokenize the text.
3. Convert tokens to input IDs.
4. Pass the IDs to the LLM.
5. Receive logits for every possible next token.
6. Restrict the logits to tokens allowed by the current output state and schema.
7. Select the next token.
8. Append it to the generated sequence and repeat until the response is complete.

Tokenization must be treated as subword tokenization, not word splitting. Tokens may contain leading-space markers, punctuation, or fragments of words. The vocabulary file is therefore important when determining what text each possible token would append.

## Constrained decoding requirements

At every generation step:

1. Obtain logits for all possible next tokens.
2. Determine which tokens preserve valid JSON syntax and the required schema.
3. Set the logits for invalid tokens to negative infinity.
4. Select only from the remaining valid tokens.

Constraints must enforce both:

- JSON syntax: objects, strings, numbers, booleans, punctuation, escaping, and termination must remain valid.
- Schema semantics: the function name, required parameter names, and parameter types must match a definition from `functions_definition.json`.

For example, when a parameter is defined as `number`, generation for its value must remain compatible with a JSON number. The final result must always be parseable and schema-compliant.

The LLM—not a heuristic—must decide which function to call. The decoder then guarantees that the chosen name and generated parameters conform to the permitted schema.

## Output

The default output path is:

```text
data/output/function_calls.json
```

The file contains one object per input prompt. Every object must contain exactly these keys:

- `prompt`: the original natural-language request as a string.
- `name`: the selected function name as a string.
- `parameters`: all required arguments as an object with the correct types.

Example:

```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {
      "s": "hello"
    }
  }
]
```

### Output validation rules

- The entire file must be valid JSON.
- Comments and trailing commas are forbidden.
- Each result object must have exactly `prompt`, `name`, and `parameters`.
- Extra keys and explanatory prose are forbidden.
- The function name must exist in the supplied definitions.
- All required arguments must be present.
- Parameter names and types must match the selected function definition exactly.
- Every output must be parseable and schema-compliant.

## Performance and reliability targets

- At least 90% accuracy for function selection and argument extraction.
- 100% valid, schema-compliant JSON.
- Process the full test input in under five minutes on standard hardware.
- Handle malformed input, missing files, and edge cases gracefully.

## Testing expectations

Minimum manual verification flow:

1. Place both input files in `data/input/`.
2. Run the module with default or explicit paths.
3. Confirm that `data/output/function_calls.json` is created.
4. Parse the output as JSON.
5. Validate its structure against the required output format.
6. Verify every function name and parameter type against the supplied definitions.

Include edge cases such as:

- Empty strings.
- Large numbers.
- Special characters and escaping.
- Incorrect input types.
- Ambiguous prompts.
- Functions with multiple parameters.
- Invalid JSON.
- Missing input files.
- Unknown or difficult-to-match requests.

Unit tests may use `pytest` or `unittest`.

## Makefile

The root `Makefile` must provide these targets:

- `install`: install dependencies with `uv`, `pip`, `pipx`, or another package manager.
- `run`: run the main program.
- `debug`: run the main program with Python's debugger, such as `pdb`.
- `clean`: remove temporary files and caches such as `__pycache__` and `.mypy_cache`.
- `lint`: run both commands below.
- `lint-strict` (optional): run `flake8 .` and `mypy . --strict`.

The mandatory `lint` commands are:

```bash
flake8 .
mypy . \
  --warn-return-any \
  --warn-unused-ignores \
  --ignore-missing-imports \
  --disallow-untyped-defs \
  --check-untyped-defs
```

## README requirements

The repository must contain an English-language `README.md` at its root.

Its first line must be italicized and use this format:

```markdown
*This project has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]].*
```

It must include:

- `Description`: project goal and overview.
- `Instructions`: installation and execution.
- `Resources`: conventional references plus a description of how and where AI was used.
- Algorithm explanation: the constrained-decoding approach in detail.
- Design decisions: important implementation choices.
- Performance analysis: accuracy, speed, and reliability.
- Challenges faced and their solutions.
- Testing strategy.
- Example usage.

## Optional bonus work

Bonus work is evaluated only when every mandatory requirement is complete and functional. Features must work and be demonstrable, not merely be documented.

Possible bonuses:

- Support multiple LLM models in addition to `Qwen/Qwen3-0.6B`.
- Reimplement tokenizer behavior so the main code avoids direct use of SDK `encode` and `decode`, relying on `get_logits_from_input_ids` and `get_path_to_vocab_file`.
- Add public tokenizer encode and optional decode implementations.
- Demonstrate how custom encoding and decoding integrate with constrained decoding.
- Add advanced error recovery.
- Optimize with caching or batching.
- Add a comprehensive test suite.
- Visualize the generation process.
- Support complex nested function arguments.

Additional libraries may be used for bonus work if their use can be justified during evaluation.

## Repository and submission requirements

Only files committed to the repository are evaluated. The repository must contain:

```text
src/                 implementation
data/input/          demonstration input files
llm_sdk/             supplied SDK package
pyproject.toml       project dependencies and configuration
uv.lock              locked dependencies
Makefile             required task automation
README.md            required project documentation
```

Do not commit `data/output/`. It must be generated during evaluation.

Check all filenames and repository contents before submission.

During evaluation, reviewers may request a small behavior change, code edit, or simple feature. Be prepared to explain and modify the implementation within a few minutes.

## AI-use expectations

- Understand and take responsibility for all submitted work.
- Review, question, and test AI-generated output.
- Be able to explain implementation decisions during evaluation.
- Use peer review as an additional validation step.
