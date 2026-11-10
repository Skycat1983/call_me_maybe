# LLM SDK Reference

Status: Learning reference  
Source: `llm_sdk/llm_sdk/__init__.py`

Learning context: [Waypoint 004](../learning/waypoints/004-2026-11-10-supplied-data-and-llm-sdk.md)

## What the SDK is

The supplied SDK wraps a Hugging Face causal language model in
`Small_LLM_Model`. It hides most model-loading details and exposes the small
public interface needed for token-by-token generation.

The SDK is model access, not the finished application. It does not:

- Read the project's input JSON files.
- Choose output paths.
- Generate a complete function-call document by itself.
- Enforce JSON or function schemas.
- Validate the final project output.

Those are responsibilities of the future `src` application.

## Installation versus model download

There are three separate layers:

1. The local `llm-sdk` Python package lives in this repository.
2. `uv sync` installs its Python dependencies, including PyTorch,
   Transformers, and Hugging Face Hub.
3. Constructing `Small_LLM_Model()` loads the Qwen tokenizer and model. If
   their files are not cached, Hugging Face downloads them at that time.

The current environment is incomplete: an import-only test found
`transformers` missing from `.venv`. It has not been fully synced with the
current lockfile, and dependency installation must finish before the SDK can
import.

Model downloads normally use the home-directory Hugging Face cache. Because
this machine has a small home partition, use a cache on the larger `/tmp`
filesystem during experiments:

```bash
HF_HOME=/tmp/call-me-maybe-huggingface \
uv run python ...
```

This is an environment decision for local development, not a project
requirement.

## Construction

```python
model = Small_LLM_Model()
```

Construction performs these steps:

1. Store the model identifier, defaulting to `Qwen/Qwen3-0.6B`.
2. Select `mps`, then `cuda`, then `cpu`, unless a device was supplied.
3. Select `float16` on MPS/CUDA or `float32` on CPU, unless a dtype was
   supplied.
4. Load the tokenizer.
5. Give the tokenizer a padding token if it lacks one.
6. Load the causal language model.
7. Move the model to the selected device.
8. Enable evaluation mode.
9. Disable gradients for every parameter.

Evaluation mode and disabled gradients are appropriate because this project
uses inference: it asks an already-trained model for predictions and does not
train the model.

## Public interface

The project may use these public members. It must not access underscore-prefixed
state such as `_model` or `_tokenizer`.

### `encode(text)`

```python
encode(text: str) -> torch.Tensor
```

Converts text into token IDs without adding special tokens.

If tokenization produces:

```python
[42, 105, 9]
```

the return value is a two-dimensional tensor resembling:

```python
tensor([[42, 105, 9]])
```

Its shape is `[1, token_count]`, where `1` is the batch size. It uses integer
dtype `torch.long` and lives on the model's selected device.

### `decode(ids)`

```python
decode(ids: torch.Tensor | list[int]) -> str
```

Converts token IDs back to text and removes special tokens. Tensor input is
converted to a Python list first.

There is an interface question to test: `encode()` returns a two-dimensional
tensor, while the underlying tokenizer normally decodes a one-dimensional
sequence. The likely round-trip form is:

```python
encoded = model.encode("hello")
text = model.decode(encoded[0])
```

This should be confirmed with a small experiment after dependencies and model
files are available.

### `get_logits_from_input_ids(input_ids)`

```python
get_logits_from_input_ids(input_ids: list[int]) -> list[float]
```

Accepts one token-ID sequence and returns raw next-token scores.

Internally:

```text
input list                       [sequence_length]
batched tensor                   [1, sequence_length]
model output logits              [1, sequence_length, vocabulary_size]
selected final-position logits   [vocabulary_size]
returned Python list             [vocabulary_size]
```

The value at index `i` is the logit for token ID `i`. A larger value means the
model considers that token more plausible as the next token. A logit is not a
probability; softmax would convert the complete set of logits into
probabilities.

For constrained decoding, invalid token indices can be assigned negative
infinity. The next token is then selected only from valid candidates.

### Tokenizer-file paths

```python
get_path_to_vocab_file() -> str
get_path_to_merges_file() -> str
get_path_to_tokenizer_file() -> str
```

Each method identifies a tokenizer filename, downloads it from the configured
model repository if necessary, and returns its local cache path.

- A vocabulary maps token text to integer IDs.
- A merges file describes how smaller pieces combine in a BPE tokenizer.
- `tokenizer.json` is a serialized representation of the complete tokenizer.

These files are absent from the project repository because they belong to the
selected model and are obtained at runtime.

## Private state

The instance manages:

| Attribute | Meaning |
|---|---|
| `_model_name` | Hugging Face model repository identifier. |
| `_device` | CPU, CUDA, or MPS computation location. |
| `_dtype` | Numeric precision used for model weights. |
| `_tokenizer` | Text/token-ID conversion implementation. |
| `_model` | Loaded causal language model. |

The subject forbids using these private attributes. Future code should depend
only on the public methods so the SDK remains replaceable.

## One-step mental model

```text
prompt text
  → encode
token IDs
  → get_logits_from_input_ids
one score per possible next token
  → mask structurally invalid token scores
valid scores only
  → choose one token ID
append that ID and repeat
```

The LLM supplies semantic preferences through its logits. The constrained
decoder supplies structural guarantees by controlling which logits remain
eligible.
