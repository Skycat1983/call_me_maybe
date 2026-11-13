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
- [`Q-002`](../../waypoints/011-2026-11-13-pydantic-input-models.md#q-002-resolved-supported-parameter-types),
  resolved in Waypoint 011:
  which schema types are mandatory?
- [`Q-003`](../../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md#resolved-questions),
  resolved in Waypoint 007:
  which tokenizer files does Qwen expose?
- [`Q-004`](../../../project/questions.md#q-004-what-prompt-format-produces-reliable-semantic-function-selection):
  how should the prompt and definitions be presented?
- [`Q-005`](../../../project/questions.md#q-005-how-should-a-per-prompt-generation-failure-be-represented):
  how should generation failure be represented?

## Voice-session review — 2026-11-13

This follow-up captures concepts the learner paused on and wants to revisit
in a later voice session. It supplements the original waypoint rather than
claiming that the application or decoder has been implemented.

### 1. Tensor, tensor shape, dtype, and device

A PyTorch tensor is a numerical array that can have zero, one, two, or more
dimensions. A two-dimensional tensor resembles a matrix, but *tensor* is the
broader term. Unlike an ordinary Python list, it supports optimized numerical
computation and records its dtype and device.

The explicit-CPU SDK probe encoded the prompt
`What is the sum of 2 and 3?` as:

```text
tensor shape:  (1, 11)
tensor dtype:  torch.int64
tensor device: cpu
token count:   11
token IDs:     [3838, 374, 279, 2629, 315, 220, 17, 323, 220, 18, 30]
```

Read `(1, 11)` as **one sequence containing eleven token IDs**. The
leading `1` is the batch dimension, not an additional token. `int64`
is the integer storage dtype of token IDs; `cpu` is the location where
this tensor is held. Encoding converts text to IDs; this alone is not
semantic interpretation of the question.

### 2. Decoding a whole batch versus one sequence

The observed results in
[Waypoint 007](../../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md)
are:

```python
model.decode(encoded)     # ['What is the sum of 2 and 3?']
model.decode(encoded[0])  # 'What is the sum of 2 and 3?'
```

`encoded` is two-dimensional, while `encoded[0]` selects its first
one-dimensional sequence. The SDK annotation `-> str` does not capture
the batched `list[str]` return; see `I-004`.

### 3. What the next-token logits actually score

**Revisit this wording:** We feed the **whole question** as a sequence
of eleven input tokens. The model uses that entire context to score
**each possible single next token after the question**. It does **not**
produce one output token or one set of logits per individual input token
in the terminal report.

The observed output contained **151,936 logits**, one per vocabulary
token ID. The probe shows only the ten highest-scoring candidate tokens,
not 151,936 numbers. Its first candidates were `' What'`, `' To'`,
and `' Also'`. These are *possible continuations following the entire
input*, not matches against individual words in the input.

A higher logit is a stronger raw model preference, **not a probability**.
The displayed ordering is a ranking. The probe did not yet select and
append a generated token.

### 4. Constrained decoding: valid prefixes, not keyword matching

The constrained decoder checks whether appending the *entire candidate
token text* leaves a prefix that can still be completed into a JSON
object satisfying the permitted function schema. A valid prefix need not
yet be complete JSON.

For example, after `{"name":"fn_`, a token continuing an allowed
function name could be eligible; a token leading irreversibly to a
nonexistent name must be rejected. A token may contain several
characters and cross more than one grammar boundary, so checking only
its first character is insufficient. These token fragments are
**illustrative**, not measured Qwen token boundaries.

A JSON-aware parser or state machine is a plausible implementation
approach to investigate, not a completed or selected design. Regex may
help with restricted values but is not by itself a complete nested JSON
and schema validator. The LLM still ranks semantic candidates; the
decoder constrains format and allowed names/types; a final validator
checks the complete result. These constraints do not guarantee that the
chosen function or argument values are semantically correct.

### 5. The iterative feedback loop

**Core recall phrase: Predict → Filter → Select → Append → Predict again.**

```text
whole prompt + all previously selected token IDs
    → get next-token logits across the vocabulary
    → mask candidates that cannot preserve a valid JSON/schema prefix
    → select an allowed token using the remaining model scores
    → append its ID to the input sequence
    → request fresh logits using the longer context
    → repeat until the output is complete
```

If the first permitted output is `{`, a token representing it can be
selected even if ordinary words originally scored higher. Once appended,
the next model call sees that bracket in its context. JSON-like
continuations, such as a quoted property name, may consequently receive
higher scores. **The decoder does not reuse the old logits for all
subsequent positions.** Prompt construction can also make JSON
continuations more plausible from the outset.

The SDK probe observed **one** next-token scoring step; this repeated
generation-and-masking loop remains a conceptual walkthrough, not a
feature already implemented or tested in the project.

### Targeted recall questions for the next voice session

1. How does a tensor differ from a normal list, and what does `(1, 11)`
   mean?
2. What do `torch.int64` and `cpu` tell us about the encoded result?
3. Why does `decode(encoded)` give a list but `decode(encoded[0])` a
   string?
4. Does each of the eleven input tokens get one of the 151,936 reported
   logits, or what do those logits actually represent?
5. Is the top-ranked token already generated? Why is a logit not a
   probability?
6. What is the difference between an incomplete *valid prefix* and a
   prefix that cannot be completed into the required JSON?
7. Why must candidate validation inspect the whole token?
8. Explain the **predict → filter → select → append → predict again**
   loop, including why appending `{` may change the model's next
   preferences.
9. Which responsibilities belong to the model, the constrained decoder,
   and the final validator?

### Session status

- Encoding, decode-shape differences, and next-token ranking were
  explained and understood during the discussion.
- Tensors/dtypes, the input-versus-next-token relationship, and the
  iterative generation loop were explicitly marked for later recall.
- The conceptual constrained-decoding discussion is sufficient for now;
  no application implementation, production device-policy decision, or
  semantic-function-selection benchmark was performed.

## Successful session outcome

The learner can explain the full one-token generation loop, distinguish
semantic model choice from structural constraints, describe the SDK's public
surface, and identify which points still require experiments rather than
guesswork.
