# Probe Experiments and Results

- Kind: Thematic talking point
- Theme: LLM SDK and `inspect_sdk`
- Depth: Runtime evidence
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: [Probe overview](index.md)

## The two real experiments

### Default device selection

Command:

```bash
make inspect-sdk
```

Observed result: model construction failed before encoding with a
`ValueError` stating that use of a `device_map` requires `accelerate`.

This failure proves that the particular automatic loading path reached during
that run needed `accelerate`. It does not prove that every platform or device
path needs it.

### Explicit CPU selection

Command:

```bash
make inspect-sdk-cpu
```

Observed result: the complete probe ran and exited successfully. Explicit CPU
was the only intended experimental change, supporting the hypothesis that the
earlier failure belonged to the automatic device-mapping path.

This does not repair or validate automatic/GPU selection. It establishes a
working CPU path for continued learning.

## Observed CPU results

### Construction

```text
model identifier: Qwen/Qwen3-0.6B
requested device: cpu
construction time: 18.419 seconds
```

### Encoding

```text
prompt: 'What is the sum of 2 and 3?'
tensor shape: (1, 11)
tensor dtype: torch.int64
tensor device: cpu
token count: 11
token IDs: [3838, 374, 279, 2629, 315, 220, 17, 323, 220, 18, 30]
```

The `1` is the batch size; `11` is the sequence length in model tokens. It is
not a count of words or characters. Integer token IDs use `torch.int64`.

### Decoding

```text
decode(encoded): ['What is the sum of 2 and 3?']
decode(encoded[0]): 'What is the sum of 2 and 3?'
```

The two-dimensional batch returned a list containing one string. The
one-dimensional sequence returned one string. This was an observed SDK
interface mismatch because the wrapper annotates `decode()` as returning
`str`, yet its own batched `encode()` output produces `list[str]` when decoded
directly.

Application code needing one string should pass one sequence, such as
`encoded[0]`, unless the supplied wrapper is deliberately repaired later.

### Tokenizer artifacts

| File | Exists | Observed size |
|---|---:|---:|
| `vocab.json` | yes | 2,776,833 bytes |
| `merges.txt` | yes | 1,671,853 bytes |
| `tokenizer.json` | yes | 11,422,654 bytes |

The paths were under the Qwen snapshot in
`/tmp/call-me-maybe-huggingface`. This confirms that all three public path
methods work with the cached Qwen3-0.6B tokenizer used in the experiment.

### Logits

```text
logit count: 151936
logits time: 0.301 seconds
```

There was one returned raw score for each token ID in the model vocabulary.
The ten highest-scoring decoded texts were:

```text
' What'
' To'
' Also'
' \n\n'
' How'
' And'
' Is'
' '
' The'
' Can'
```

These ordinary prose fragments do not indicate a broken model. The prompt
only asked a natural-language question. It did not tell the model:

- which functions are available;
- what those functions do;
- which arguments they accept;
- that it must choose a function;
- that output must follow a JSON schema;
- what prefix or chat template is required.

The run therefore tested next-token scoring, not semantic function selection.

## What the experiment proves—and what it does not

### Supported by execution

- the explicit CPU constructor path works in the tested environment;
- the prompt encodes to the recorded tensor and token IDs;
- direct batched decode and single-sequence decode have different return
  container types;
- all three tokenizer files exist through the public interface;
- one CPU forward pass returns 151,936 logits;
- the top candidates for the bare prompt are ordinary text fragments;
- deleting the `/tmp` environment is recoverable because `uv` recreated it.

### Not established

- that automatic device selection or CUDA now works;
- that adding `accelerate` is the correct long-term repair;
- that the model can yet choose the correct project function;
- that constrained decoding or JSON validation works;
- that the timings are stable benchmarks;
- that every prompt produces 11 tokens or every model has this vocabulary;
- that the experiment is production-ready application architecture.

## Related learning

- [LLM-SDK theme home](../index.md)
- [Probe source walkthrough](source-walkthrough.md)
- [Questions and discussion](questions-and-discussion.md)
- [Detailed runtime flow](../runtime-flow/index.md)
- [Waypoint 007](../../../../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md)

