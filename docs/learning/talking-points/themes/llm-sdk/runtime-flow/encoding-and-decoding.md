# Runtime Flow: Encoding and Decoding

- Kind: Thematic talking point
- Theme: LLM SDK and `inspect_sdk`
- Depth: Detailed execution stages 7–10
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: [Model construction](model-construction.md)

## Stage 7: Encode the prompt

The script calls:

```python
encoded = model.encode(PROMPT)
```

### Inside `encode()`

The method parameter `text` receives the same string object referenced by
`PROMPT`.

```python
ids = self._tokenizer.encode(text, add_special_tokens=False)
```

`ids` is a local `list[int]`. Each integer identifies one tokenizer vocabulary
entry. `add_special_tokens=False` means this wrapper does not automatically
add beginning/end or chat-control tokens.

For the recorded prompt:

```text
ids = [3838, 374, 279, 2629, 315, 220, 17, 323, 220, 18, 30]
length = 11
```

The return statement builds:

```python
torch.tensor([ids], device=self._device, dtype=torch.long)
```

Why `[ids]` rather than `ids`?

- `ids` alone represents one sequence with shape `(11,)`;
- `[ids]` wraps it in a batch with shape `(1, 11)`.

`torch.long` is PyTorch's 64-bit integer dtype, appropriate for discrete token
indices. The device is the same backend selected during construction.

### Back in the probe

```text
encoded
type: torch.Tensor
shape: (1, 11)
dtype: torch.int64 / torch.long
device: cpu
meaning: batch of one token-ID sequence
```

The tensor holds numbers, not the original string. The tokenizer can later
translate those IDs back to text.

## Stage 8: Select one sequence and convert it to a list

```python
input_ids = encoded[0].tolist()
```

This expression is evaluated from left to right:

1. `encoded[0]` selects batch row zero;
2. its shape changes from `(1, 11)` to `(11,)`;
3. `.tolist()` copies its values into ordinary Python data;
4. `input_ids` receives `list[int]`.

Variable state:

```text
encoded           Tensor, shape (1, 11), remains unchanged
encoded[0]        temporary Tensor view/selection, shape (11,)
input_ids         Python list[int], length 11
```

The learner is not expected to know `.tolist()` from memory. It is discoverable
because `encode()` announces `torch.Tensor` as its return type. Hover,
completion, F12, `help(torch.Tensor.tolist)`, installed docs, or library docs
can reveal the method.

## Stage 9: Print encoding metadata

The reporting expressions do not modify the tensor.

| Expression | Result |
|---|---|
| `PROMPT!r` | Python representation including quotes and escapes |
| `tuple(encoded.shape)` | `(1, 11)` for concise display |
| `encoded.dtype` | `torch.int64` |
| `encoded.device` | `cpu` |
| `len(input_ids)` | `11` |

`encoded.shape` already contains the dimensions as `torch.Size([1, 11])`.
Converting it to a tuple is optional presentation formatting.

## Stage 10: Decode two different shapes

The first call passes the full batched tensor:

```python
direct_decoded = model.decode(encoded)
```

Inside `decode()`:

```python
if isinstance(ids, torch.Tensor):
    ids = ids.tolist()
```

For the batched input, `.tolist()` produces a nested list:

```text
[[3838, 374, ..., 30]]
```

The tokenizer receives that nested structure. The recorded library behavior
returned:

```text
['What is the sum of 2 and 3?']
```

The second call passes only row zero:

```python
row_decoded = model.decode(encoded[0])
```

This conversion produces a flat list:

```text
[3838, 374, ..., 30]
```

The recorded result was one string:

```text
'What is the sum of 2 and 3?'
```

### Interface mismatch

The source annotation says `-> str`, but observed batched input returned
`list[str]`. For one decoded string, project code should pass one sequence.

### Why separate `try` blocks?

The two forms are independent questions. If the batched call fails, the probe
still tests the single-sequence form. Each exception is caught in local
variable `error` and printed with its class name and message.

The exception handlers are diagnostic policy, not necessarily suitable
application error handling.

## Related learning

- [Runtime-flow map](index.md)
- [Previous: model construction](model-construction.md)
- [Next: tokenizer files](tokenizer-files.md)
- [SDK reference](../../../../../reference/llm-sdk.md)

