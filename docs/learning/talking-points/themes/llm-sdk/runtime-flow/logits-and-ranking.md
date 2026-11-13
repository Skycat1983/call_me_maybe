# Runtime Flow: Logits and Candidate Ranking

- Kind: Thematic talking point
- Theme: LLM SDK and `inspect_sdk`
- Depth: Detailed execution stages 12–15
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: [Tokenizer files](tokenizer-files.md)

## Stage 12: Request next-token logits

The script calls:

```python
logits = model.get_logits_from_input_ids(input_ids)
```

### Inside the SDK method

The input crosses from ordinary Python data back into PyTorch:

```python
input_tensor = torch.tensor(
    [input_ids],
    device=self._device,
    dtype=torch.long,
)
```

```text
input_ids       list[int], length 11
input_tensor    Tensor, shape (1, 11), int64, CPU
```

The model is called inside:

```python
with torch.no_grad():
    out = self._model(input_ids=input_tensor)
```

`torch.no_grad()` temporarily disables gradient recording. `out` is a
Transformers model-output object, not just a list. Its `.logits` member holds
scores for every sequence position and every vocabulary token.

Observed conceptual shape:

```text
out.logits
shape: (1, 11, 151936)
axes:  batch, sequence position, vocabulary token
```

Then:

```python
out.logits[0, -1]
```

selects:

- batch member `0`: the only prompt;
- sequence position `-1`: the final prompt token;
- all vocabulary entries: every possible next token.

The result is a one-dimensional tensor of length 151,936.

`.tolist()` converts it to Python numbers. The final list comprehension
ensures each element is a built-in `float`:

```python
return [float(x) for x in logits]
```

### Back in the probe

```text
logits
type: list[float]
length: 151936
meaning: one raw next-token score for every token ID
observed CPU calculation time: 0.301 seconds
```

The index of each score is its token ID:

```text
logits[3555] is the score for token ID 3555
```

### Logits are not probabilities

Logits are unrestricted raw comparative scores. They need not lie between
zero and one and do not sum to one. Softmax could convert the entire vector to
probabilities, but ranking does not require it because softmax preserves order.

## Stage 13: Find the ten highest-scoring token IDs

```python
top_token_ids = nlargest(
    TOP_CANDIDATE_COUNT,
    range(len(logits)),
    key=logits.__getitem__,
)
```

Breakdown:

```text
TOP_CANDIDATE_COUNT     10
len(logits)             151936
range(len(logits))      candidate IDs 0 through 151935
logits.__getitem__      function that returns logits[index]
top_token_ids           ten indices with the greatest associated scores
```

Ranking indices rather than score values preserves the token IDs needed for
decoding.

`nlargest` avoids fully sorting all 151,936 candidates when only ten are
needed.

## Stage 14: Decode and print each candidate

The loop assigns three important names:

```python
for rank, token_id in enumerate(top_token_ids, start=1):
    token_text = model.decode([token_id])
```

| Variable | Type | Meaning |
|---|---|---|
| `rank` | `int` | Human-facing position 1 through 10 |
| `token_id` | `int` | Vocabulary index selected from logits |
| `token_text` | `str` | Readable fragment for that one token |

`[token_id]` is a one-element sequence because `decode()` expects a sequence
of IDs, even when decoding one token.

The print formatting controls alignment only:

- `{rank:>2}`: right-align rank in width two;
- `{token_id:<7}`: left-align ID in width seven;
- `{logits[token_id]:>10.4f}`: width ten, four decimal places;
- `{token_text!r}`: representation showing spaces and newlines explicitly.

The recorded top fragments began with ordinary prose such as `' What'`,
`' To'`, and `' Also'`. The prompt contained no function definitions or JSON
instruction, so this experiment did not test function selection.

## Stage 15: Process completion

After the loop:

1. `main()` reaches its end and returns `None`;
2. the module guard has no more work;
3. Python exits with status zero if no uncaught exception occurred;
4. the in-memory SDK object, tokenizer, model, tensors, and lists are released;
5. installed packages and cached model files remain on disk for later runs.

An uncaught constructor or logits exception instead produces a traceback and
nonzero process status, making an incomplete experiment visible.

## Related learning

- [Runtime-flow map](index.md)
- [Previous: tokenizer files](tokenizer-files.md)
- [Next: variable ledger and discussion](variable-ledger-and-discussion.md)
- [Constrained decoding requirements](../../../../../requirements/constrained-decoding.md)

