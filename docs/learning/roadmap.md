# Learning Roadmap

This roadmap orders the work so concepts are understood before they are used
in implementation.

## 1. Supplied data and SDK

- Understand the prompt and function-definition files.
- Understand how Python resolves the SDK's dependencies.
- Understand model construction, tokenization, logits, and vocabulary files.
- Run small experiments that confirm the documented interface.

## 2. Application boundaries

- Identify CLI, loading, validation, generation, and output responsibilities.
- Decide what can be tested without loading the model.
- Document component inputs, outputs, and owned errors.

Expected document: `docs/design/architecture.md`.

## 3. Reliable input and output

- Create the module entry point.
- Parse CLI arguments.
- Model input and output with Pydantic.
- Handle missing files, invalid JSON, and invalid schemas.
- Test the shell of the application without generation.

## 4. Tokens and partial validity

- Inspect real token IDs and decoded token text.
- Distinguish complete, incomplete-but-possible, and impossible JSON prefixes.
- Design a small state machine for one fixed function call.
- Test multi-character and whitespace-bearing tokens.

## 5. Constrained decoding

- Restrict fixed JSON syntax.
- Restrict function names to the supplied set.
- Restrict parameter names and required fields.
- Add string, number, boolean, and other required value states.
- Define valid completion and stopping behavior.

## 6. LLM integration

- Supply prompt and function context to the model.
- Retrieve next-token logits.
- Mask invalid candidates.
- Select the best valid token.
- Append it and repeat.
- Verify that semantic selection comes from model scores rather than
  application heuristics.

## 7. Evaluation

- Measure selection and argument accuracy.
- Verify 100% JSON and schema validity.
- Measure runtime.
- Test replacement function sets.
- Complete the README and evaluation checklist.

At every stage, use this loop:

```text
explain → inspect → predict → experiment → implement → test → document
```
