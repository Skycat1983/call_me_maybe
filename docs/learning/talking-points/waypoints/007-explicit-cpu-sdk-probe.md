# Talking Points 007: Explicit-CPU SDK Probe

Companion waypoint:
[007 — Explicit-CPU SDK probe](../../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md)

Detailed topic briefing:
[`inspect_sdk.py` probe overview](../themes/llm-sdk/probe/index.md)

Living execution walkthrough:
[full `inspect_sdk` flow](../themes/llm-sdk/runtime-flow/index.md)

## Agent preparation

Read:

- the companion waypoint;
- `experiments/inspect_sdk.py`;
- [LLM SDK reference](../../../reference/llm-sdk.md);
- [open questions](../../../project/questions.md);
- [known issues](../../../project/issues.md).

Discuss observed behavior before proposing application design. Do not begin a
generation loop or prompt implementation during this session.

## Short recap

Explicit CPU selection changed one variable and allowed the model to load.
The complete public-interface probe then observed encoding, decoding,
tokenizer files, and one logits vector.

## Conversation order

1. Why explicit CPU was a controlled experiment.
2. Model construction and cache behavior.
3. Token tensor shape, dtype, and device.
4. The two decode return values.
5. Tokenizer-file evidence.
6. Logits shape, timing, and top candidates.
7. Why a bare prompt did not produce function-call tokens.
8. Remaining device and prompt-design questions.

## Key observations

| Observation | Interpretation |
|---|---|
| Construction succeeded in 18.419 seconds | Current dependencies work on explicit CPU. |
| Shape `(1, 11)` | One batch containing an 11-token sequence. |
| `torch.int64` | Token IDs are stored as integers. |
| Direct decode returned `list[str]` | The SDK return annotation is not always accurate. |
| Row decode returned `str` | A single token-ID sequence gives one string. |
| Three tokenizer files exist | Public path methods work for Qwen3-0.6B. |
| 151,936 logits | One raw score exists per vocabulary token ID. |
| Logits took 0.301 seconds | One CPU forward pass is fast enough for experiments. |
| Top tokens were natural-language fragments | The bare prompt lacked function definitions and output instructions. |

## Discussion prompts

- What is the difference between `make -n inspect-sdk-cpu` and
  `make inspect-sdk-cpu`?
- Which output proves that the Python experiment actually reached the model?
- Why is explicit CPU a better first test than immediately adding a package?
- What evidence supports the automatic-device-path hypothesis?
- What remains unproven about default or GPU behavior?
- What does the `1` mean in shape `(1, 11)`?
- Why are token IDs represented as `int64`?
- Why did `decode(encoded)` return a list?
- Which return value matches the SDK annotation?
- What should project code pass to `decode()` when it needs one string?
- How do `vocab.json`, `merges.txt`, and `tokenizer.json` differ?
- Why does 151,936 logits imply 151,936 candidate token IDs?
- Why are raw logits not probabilities?
- Why did the highest-scoring tokens look like normal prose?
- What information must a future model prompt include?

## Understanding checks

### Trace the observed data

Ask the learner to narrate:

```text
question string
→ 11 token IDs
→ tensor shaped (1, 11)
→ model forward pass
→ 151,936 next-token logits
→ rank candidate IDs
→ decode individual candidate IDs
```

### Explain the decode mismatch

Ask why these differ:

```python
model.decode(encoded)     # list[str]
model.decode(encoded[0])  # str
```

The answer should mention batch dimensionality rather than different text
content.

### Explain the prompt limitation

Ask the learner to identify what the model does not know from:

```text
What is the sum of 2 and 3?
```

It has not been told the available function names, their descriptions, their
parameters, or the required output structure.

## Likely misconceptions

- Explicit CPU success does not prove default/GPU loading is fixed.
- A tensor's batch dimension is not a token.
- `decode(encoded)` returning a list is not the same as returning an
  incorrectly decoded string.
- A logit count is vocabulary size, not prompt length.
- The most likely raw continuation is not automatically a function call.
- Constrained decoding cannot select a function the model was never told
  exists.
- Probabilities sum to one; raw logits have no such requirement.
- The 0.301-second forward pass is only one token step, not full generation.

## Decisions to discuss

1. Continue local learning experiments with explicit CPU?
2. Defer automatic/GPU support until mandatory CPU behavior works?
3. Treat the decode dimensionality mismatch defensively in project code or
   repair the copied SDK?
4. What minimum prompt context should the next experiment provide?

## Successful session outcome

The learner can explain every observed tensor and return value, why explicit
CPU isolated the earlier problem, and why prompt construction is the next
conceptual topic before constrained generation.
