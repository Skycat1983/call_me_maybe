# Waypoint 007: Explicit-CPU SDK Probe

- Date: 2026-11-12
- Stage: SDK runtime experiment
- Status: Complete

Voice discussion: [Talking points 007](../talking-points/007-explicit-cpu-sdk-probe.md)

## Purpose

Test the smallest controlled change after the default constructor failed:
retain the current dependencies and pass the public constructor argument
`device="cpu"`.

If this succeeded, the same probe would continue through encoding, decoding,
tokenizer-file inspection, and one next-token logits call.

## Hypothesis

The earlier failure occurred on an automatic device-loading path that required
`accelerate`. Explicit CPU selection would avoid automatic CUDA device mapping
without changing dependencies or SDK implementation.

Supporting result:

- model construction succeeds on explicit CPU.

Rejecting result:

- the same `accelerate` error occurs even with explicit CPU.

## Controlled change

The experiment gained an optional device argument:

```bash
make inspect-sdk-cpu
```

This runs:

```bash
uv run python experiments/inspect_sdk.py --device cpu
```

The default `make inspect-sdk` remains unchanged and preserves the earlier
failure for comparison.

## Environment recreation

The `/tmp` environment had been cleared between sessions. Running the target
recreated it from `pyproject.toml` and `uv.lock`, confirming the design from
Waypoint 005.

After installation:

```text
Python environment: 5.5 GB
uv package cache:    5.4 GB
Hugging Face cache:  1.5 GB
```

These generated files remain outside the home filesystem.

## Results

### Model construction

```text
model identifier: Qwen/Qwen3-0.6B
requested device: cpu
construction time: 18.419 seconds
```

The model loaded successfully. The explicit CPU hypothesis is supported.

This result does not yet prove whether the earlier automatic path selected
CUDA or whether supplied dependency versions would behave differently. It
does prove that `accelerate` is not required for this explicit CPU path.

### Encoding

Input:

```text
What is the sum of 2 and 3?
```

Observed:

```text
tensor shape:  (1, 11)
tensor dtype:  torch.int64
tensor device: cpu
token count:   11
token IDs:     [3838, 374, 279, 2629, 315, 220, 17, 323, 220, 18, 30]
```

This confirms:

- one prompt is represented as a batch containing one sequence;
- token IDs are integers;
- the tensor is placed on the explicitly selected CPU;
- the prompt is 11 model tokens, not 11 words or characters.

### Decoding

Direct batched tensor:

```text
decode(encoded): ['What is the sum of 2 and 3?']
```

First sequence only:

```text
decode(encoded[0]): 'What is the sum of 2 and 3?'
```

The earlier prediction that direct decode would raise an exception was wrong.
Instead, the underlying tokenizer batch-decodes the two-dimensional input and
returns a list containing one string.

This exposes an SDK interface inconsistency:

- the method is annotated `-> str`;
- its docstring describes a text string;
- a 2-D tensor from the SDK's own `encode()` returns `list[str]`;
- a 1-D tensor or `list[int]` returns `str`.

Project code should pass a single sequence such as `encoded[0]` when it needs
a string. The mismatch is tracked as `I-004`.

### Tokenizer files

All three public methods succeeded:

| File | Exists | Size |
|---|---:|---:|
| `vocab.json` | yes | 2,776,833 bytes |
| `merges.txt` | yes | 1,671,853 bytes |
| `tokenizer.json` | yes | 11,422,654 bytes |

They were cached under the Qwen snapshot in
`/tmp/call-me-maybe-huggingface`.

This resolves `Q-003`: Qwen3-0.6B provides all three files requested by the
SDK.

### Next-token logits

Observed:

```text
logit count: 151936
logits time: 0.301 seconds
```

The vector contains one score per token ID in the model vocabulary.

The ten highest-scoring token texts were:

```text
 1. ' What'
 2. ' To'
 3. ' Also'
 4. ' \n\n'
 5. ' How'
 6. ' And'
 7. ' Is'
 8. ' '
 9. ' The'
10. ' Can'
```

These are ordinary text continuations rather than a function name or JSON
opening. That is expected because the input contained only the bare user
question. It did not include:

- available function definitions;
- instructions to return a function call;
- the required JSON prefix or schema;
- a chat template.

The experiment therefore demonstrates model scoring, not function-calling
quality. It strengthens `Q-004`: prompt construction is necessary before
semantic function selection can be evaluated.

## Questions and answers

### Did Make only display a command, or did the experiment really run?

The experiment really ran.

The Makefile target is:

```make
inspect-sdk-cpu:
	uv run python experiments/inspect_sdk.py --device cpu
```

`make inspect-sdk-cpu` executed that recipe. Python then reached the module
guard at the bottom of the file and called `main()`.

The earlier `make -n inspect-sdk-cpu` command was different: `-n` is a dry-run
flag that prints the recipe without executing it. It was used only to validate
the command before the real run.

Evidence that the real run executed includes:

- package and model downloads;
- 311 model-weight entries loading;
- measured construction and logits timings;
- actual token IDs and tensor properties;
- returned decode values;
- verified tokenizer file paths and sizes;
- 151,936 returned logits;
- process exit code `0`.

### Which SDK calls genuinely ran?

In order:

1. `Small_LLM_Model(device="cpu")` constructed and loaded the model.
2. `model.encode(PROMPT)` returned the prompt tensor.
3. `model.decode(encoded)` tested batched input.
4. `model.decode(encoded[0])` tested one sequence.
5. All three tokenizer path methods returned files.
6. `model.get_logits_from_input_ids(input_ids)` performed one model forward
   pass.
7. `model.decode([token_id])` decoded each of the ten highest-scoring token
   IDs.

The experiment did not call a complete generation method because the SDK does
not provide one. It also did not implement a token loop, constrained decoding,
function selection, or output JSON.

### Did explicit CPU solve model construction?

Yes, for the current environment. No additional package or SDK code change was
needed.

### Is the earlier issue fully resolved?

Not for default or GPU behavior. Explicit CPU provides a confirmed path for
learning experiments, while production device policy remains undecided.

### Does one logit call generate an answer?

No. It scores only the next token. Complete generation requires selecting one
valid token, appending it to the input IDs, and repeating.

### Why did the top tokens not mention `fn_add_numbers`?

The model was not told that `fn_add_numbers` exists. It saw only a normal
question, so it ranked plausible natural-language continuations.

### Are logits probabilities?

No. They are raw scores and need not sum to one. Softmax would transform the
complete vector into probabilities that sum to one, or 100 percent when
expressed as percentages.

## Resolved questions

- `Q-001`: direct 2-D decode returns `list[str]`; one-sequence decode returns
  `str`.
- `Q-003`: all three tokenizer files exist for Qwen3-0.6B.
- `Q-006`: explicit CPU was the next controlled strategy and succeeded.

## New or remaining questions

- `Q-002`: mandatory schema types.
- `Q-004`: prompt format for semantic function selection.
- `Q-005`: per-prompt failure representation.
- `Q-007`: production device/dependency policy.
- `I-003`: automatic/default model loading remains unresolved.
- `I-004`: `decode()` return type varies with tensor dimensionality.

## Decisions

- Use explicit CPU for the next learning experiments on this machine.
- Do not add `accelerate` merely to continue CPU investigation.
- Keep the default probe as a reproducible comparison.
- Treat the decoder return mismatch as an SDK issue, not as desired
  application behavior.
- Do not evaluate function selection from a bare user prompt.
- Discuss prompt construction before implementing a generation loop.

## Files created or updated

- `experiments/inspect_sdk.py`
- `experiments/README.md`
- `Makefile`
- `docs/project/questions.md`
- `docs/project/issues.md`
- `docs/reference/llm-sdk.md`
- `docs/project/status.md`
- `docs/project/tasks.md`
- `docs/learning/index.md`
- `docs/learning/talking-points/index.md`

## Next step

Discuss the evidence in voice mode. The next technical topic is prompt
construction: what context the model needs to rank available function names
without replacing semantic selection with application heuristics.
