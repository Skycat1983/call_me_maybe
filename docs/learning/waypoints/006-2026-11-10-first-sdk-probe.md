# Waypoint 006: First SDK Probe

- Date: 2026-11-10
- Stage: SDK runtime experiment
- Status: Paused for discussion after a reproducible constructor failure

Voice discussion: [Talking points 006](../talking-points/006-first-sdk-probe.md)

## Purpose

Run the first evidence-generating experiment against the supplied SDK without
writing application or constrained-decoding code.

The intended probe would:

1. Construct `Small_LLM_Model`.
2. Inspect `encode()` output.
3. Compare both possible `decode()` inputs.
4. Inspect tokenizer files through public methods.
5. Request one logits vector and decode its highest-scoring tokens.

## Topics covered

- Designing a reusable learning experiment.
- Validating experiment code before running it.
- Sequential failure: later observations are unavailable when construction
  fails.
- The Transformers `device_map` and `accelerate` relationship.
- Supplied lockfile versions versus newly resolved versions.
- Recording a failure as evidence rather than immediately patching around it.

## Progress made

- Added `experiments/inspect_sdk.py`.
- Added `experiments/README.md`.
- Added `make inspect-sdk`.
- Verified the probe with Python compilation and targeted Flake8.
- Ran the probe with package, environment, and Hugging Face storage under
  `/tmp`.
- Reproduced a model-construction error.
- Confirmed that no Qwen model weights were downloaded.
- Compared dependency versions in the supplied SDK lockfile and root lockfile.

## Predictions before the run

- Construction would download the Qwen tokenizer and model under `HF_HOME`.
- The selected device would probably be CPU because no usable NVIDIA driver
  was visible in the initial system check.
- `encode()` would return a two-dimensional integer tensor.
- `decode(encoded)` might fail while `decode(encoded[0])` would work.
- The logits list length would equal the tokenizer vocabulary size.

Only the construction prediction was reached. Construction began downloading
small model metadata, then failed before model weights loaded.

## Experiment design

The probe uses only the SDK's public interface:

- constructor;
- `encode`;
- `decode`;
- tokenizer path methods;
- `get_logits_from_input_ids`.

It does not access `_model`, `_tokenizer`, `_device`, or other private state.
The top logits would be ranked with Python's standard library and decoded
through the public `decode()` method.

## Actual result

The probe stopped inside `Small_LLM_Model()`:

```text
ValueError: Using a `device_map`, `tp_plan`, `torch.device` context manager
or setting `torch.set_default_device(device)` requires `accelerate`.
You can install it with `pip install accelerate`
```

The call path was:

```text
Small_LLM_Model()
→ AutoModelForCausalLM.from_pretrained(...)
→ check_and_set_device_map(...)
→ ValueError
```

The later encoding, decoding, tokenizer-path, and logits sections did not run.
Their questions remain open.

## Evidence gathered

### Environment

- The relocated environment is complete enough to import `llm_sdk`.
- Installed Transformers version: `5.20.2`.
- Installed PyTorch version for Python 3.10: `2.14.1`.
- `accelerate` is not installed.

### Supplied versus root lock

The supplied `llm_sdk/uv.lock` records:

```text
transformers 5.0.0
torch        2.10.0
accelerate   absent
```

The root `uv.lock` resolved for Python 3.10:

```text
transformers 5.20.2
torch        2.14.1
accelerate   absent
```

The SDK's broad constraints—`transformers>=4.40.0` and `torch>=2.0.0`—allow
the root resolver to select versions newer than the supplied lock.

### Hugging Face cache

Approximately 16 MB of tokenizer/configuration metadata was cached under:

```text
/tmp/call-me-maybe-huggingface
```

No large model-weight file was present after the failure.

### Installed Transformers check

The installed `check_and_set_device_map` function raises when a non-null
device map or detected non-default device is used without `accelerate`.

The SDK supplies:

```python
device_map="auto" if self._device == "cuda" else None
```

The experiment did not print the chosen SDK device before the constructor
failed, and private state must not be inspected. It is therefore not yet
proven whether the failing process selected CUDA or another loading context
caused a non-null device map.

## Questions and answers

### Did `uv sync` fail again?

No. Package synchronization completed and the SDK imported. The new failure
occurred later, during model construction inside Transformers.

### Did Qwen itself fail to generate output?

No. Model weights were not loaded, so no inference or generation occurred.
This is a model-loading dependency/compatibility problem.

### Why did none of the encode/decode output appear?

The script is sequential. `Small_LLM_Model()` must return an instance before
the public methods can be called. Its exception stopped the remaining probe.

### Should `accelerate` simply be installed?

Not without discussion. It may be the correct missing transitive dependency
for the SDK's automatic CUDA loading path, but:

- the supplied SDK does not declare it;
- the supplied lockfile also omits it;
- it is another Hugging Face package in a project with dependency
  restrictions;
- restoring supplied versions or explicitly testing CPU behavior may be more
  appropriate.

The alternatives need evidence and a documented decision.

### Does the newer Transformers version cause the failure?

It is a plausible compatibility factor, not yet a proven cause. The supplied
and root versions differ substantially, but the supplied SDK also uses
`device_map="auto"` on CUDA, a feature associated with `accelerate`. A
controlled comparison is needed.

## Options for the next experiment

These are discussion options, not decisions:

1. Run the current environment with public constructor argument
   `device="cpu"` to test whether avoiding automatic CUDA mapping succeeds.
2. Reproduce the supplied SDK lock versions in a separate `/tmp` environment
   and rerun the default constructor.
3. Add `accelerate` only if the SDK's intended loading path and project rules
   justify it.
4. Compare a small matrix: current/supplied versions and default/explicit CPU.

The safest learning order is explicit CPU first, then a supplied-version
comparison if needed. Neither requires changing production application code.

## Decisions

- Stop after the first reproducible constructor failure.
- Do not add `accelerate` automatically.
- Do not alter SDK loading logic before discussing the evidence.
- Preserve the probe so every follow-up uses the same observation code.
- Track the loading failure separately from the earlier environment-sync
  issue.

## Open questions or issues

- `Q-001` through `Q-005` remain open because later probe stages did not run.
- `Q-006`: which compatibility strategy should be tested and adopted?
- `I-003`: default SDK construction requires `accelerate` in the observed
  runtime path.

## Documents and files created or updated

- `experiments/inspect_sdk.py`
- `experiments/README.md`
- `Makefile`
- `docs/project/questions.md`
- `docs/project/issues.md`
- `docs/project/status.md`
- `docs/project/tasks.md`
- `docs/reference/llm-sdk.md`
- `docs/learning/index.md`
- `docs/learning/talking-points/index.md`

## Next step

Discuss the failure and the four experiment options in voice mode. After that
discussion, run the agreed controlled experiment and record it as Waypoint 007.
