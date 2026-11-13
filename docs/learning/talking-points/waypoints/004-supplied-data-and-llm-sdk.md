# Talking Points 004: Supplied Data and LLM SDK

Companion waypoint:
[004 — Supplied data and LLM SDK](../../waypoints/004-2026-11-10-supplied-data-and-llm-sdk.md)

## Agent preparation

Read:

- the companion waypoint;
- [LLM SDK reference](../../../reference/llm-sdk.md);
- [Python import resolution](../../../reference/imports.md);
- [open questions](../../../project/questions.md);
- the two files under `data/input/`.

This is a discussion session. Ask the learner to explain first, use small
examples, and do not load the model or implement the decoder unless explicitly
requested.

## Short recap

The supplied prompt and function-definition files were inspected. The SDK's
constructor, public methods, private state, imports, device selection, dtype,
encoding, decoding, and logits were explained. An import-only experiment
showed that the environment is not fully synced.

## Conversation order

Use this order so each idea supports the next:

1. Input prompts and function definitions.
2. Semantic function selection.
3. SDK construction and model download.
4. Tokens and token IDs.
5. Encoding and decoding.
6. Logits and next-token prediction.
7. Constrained decoding.
8. Public versus private SDK boundaries.
9. Open questions and experiments.

## Key concepts to discuss

### Data contracts

- Prompt file: array of objects containing `prompt` strings.
- Definition file: array of functions with names, descriptions, parameters,
  and return schemas.
- Current schema examples use `string` and `number`.
- Evaluation may replace both files.

### Model loading

- `uv sync` installs Python libraries.
- `Small_LLM_Model()` constructs the SDK wrapper.
- `from_pretrained(...)` loads or downloads tokenizer and model files.
- The model cache is separate from the virtual environment.
- Device means computation location; dtype means numeric precision.

### Tokens

- A token is a vocabulary unit, not necessarily a word or character.
- Text is encoded into integer token IDs.
- `encode()` returns a tensor shaped `[1, token_count]`.
- Generated token IDs are appended to the input sequence for the next step.

### Logits

- The model produces one raw next-token score per vocabulary item.
- The SDK returns a one-dimensional list of length `vocabulary_size`.
- Index `i` is the score for token ID `i`.
- Higher means more plausible, not automatically valid.

### Constrained decoding

- The LLM provides semantic ranking.
- The decoder provides structural and schema restrictions.
- Invalid token logits become negative infinity.
- Function choice may not be replaced by keyword rules.
- Generation repeats token by token.

### SDK boundary

- Public methods may be called.
- Underscore-prefixed state is private and forbidden by the subject.
- Tokenizer files are obtained through public path methods.

## Discussion prompts

- Describe both input files without looking at them.
- Map one supplied prompt to a function call and explain each argument type.
- Why is `if "sum" in prompt` not an acceptable selection strategy?
- Where is Qwen before and after `Small_LLM_Model()` is constructed?
- Explain the difference between a package dependency and model weights.
- What does the leading `1` mean in `[1, token_count]`?
- Give three examples of text that might be represented by one token.
- Explain a logit without using the word “probability.”
- Why can the most likely token still be invalid?
- What happens to an invalid token's logit?
- Why does each selected token become part of the next input?
- What is the difference between `_tokenizer` and
  `get_path_to_tokenizer_file()` from the project's point of view?

## Understanding checks

### Trace one conceptual step

Ask the learner to narrate:

```text
prompt text
→ token IDs
→ model logits
→ invalid-token masking
→ chosen valid token
→ longer token-ID sequence
```

### Classify responsibility

| Responsibility | Owner |
|---|---|
| Rank semantically likely next tokens | LLM |
| Reject invalid JSON continuations | Constrained decoder |
| Validate completed application data | Pydantic/final validator |
| Convert text to IDs | Tokenizer through SDK |
| Load input files and CLI paths | Future application shell |

### Explain partial validity

Discuss why each prefix is incomplete but may still be valid:

```text
{
{"name
{"name":
{"name":"fn_
```

Contrast it with a prefix that cannot be completed under the required schema.

## Likely misconceptions

- Model libraries and model weights are installed/downloaded at different
  times.
- A token is not the same as a word.
- A logit is not yet a probability.
- Constrained decoding does not semantically choose the function by itself.
- JSON validation only after generation is not constrained decoding.
- Python's underscore privacy is conventional, but the project rules make the
  restriction explicit.
- A lockfile can be correct while the current environment is incomplete.

## Questions raised at this waypoint

- [`Q-001`](../../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md#resolved-questions),
  resolved in Waypoint 007:
  does `decode(encode(text))` require indexing the first batch?
- [`Q-002`](../../../project/questions.md#q-002-which-parameter-schema-types-must-be-supported):
  which schema types are mandatory?
- [`Q-003`](../../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md#resolved-questions),
  resolved in Waypoint 007:
  which tokenizer files does Qwen expose?
- [`Q-004`](../../../project/questions.md#q-004-what-prompt-format-produces-reliable-semantic-function-selection):
  how should the prompt and definitions be presented?
- [`Q-005`](../../../project/questions.md#q-005-how-should-a-per-prompt-generation-failure-be-represented):
  how should generation failure be represented?

## Successful session outcome

The learner can explain the full one-token generation loop, distinguish
semantic model choice from structural constraints, describe the SDK's public
surface, and identify which points still require experiments rather than
guesswork.
