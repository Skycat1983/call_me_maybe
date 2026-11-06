# Requirements Overview

Status: Active  
Source: Call Me Maybe subject, version 1.7

## Objective

Build a function-calling tool that translates natural-language prompts into structured function calls.

For this prompt:

```text
What is the sum of 40 and 2?
```

the result must identify the function and typed arguments rather than calculate and return the answer:

```json
{
  "name": "fn_add_numbers",
  "parameters": {
    "a": 40.0,
    "b": 2.0
  }
}
```

## Core behavior

The system must:

1. Read natural-language prompts and available function definitions from JSON files.
2. Use the LLM to select the appropriate function.
3. Extract every required argument with the type declared by that function.
4. Use constrained decoding to guarantee valid, schema-compliant JSON.
5. Write one structured result per input prompt.

Function selection must come from the LLM. Hardcoded prompt mappings, keyword heuristics, and other rule-based substitutes are forbidden.

## Acceptance targets

- At least 90% correct function selection and argument extraction.
- 100% parseable, schema-compliant JSON output.
- Complete the supplied workload in under five minutes on standard hardware.
- Handle malformed input, missing files, and edge cases without an unexpected crash.
- Work with the required `Qwen/Qwen3-0.6B` model.

## Requirement map

- [Implementation rules](implementation-rules.md): environment, permitted dependencies, quality rules, Makefile, and repository layout.
- [Input/output contract](input-output-contract.md): command line, files, schemas, and error behavior.
- [Constrained decoding](constrained-decoding.md): the mandatory token-generation behavior.
- [Evaluation checklist](evaluation-checklist.md): completion and submission review.
