# Learning Experiments

These programs investigate supplied components before production design begins.
They are evidence-generating tools, not application implementation.

## SDK probe

Run:

```bash
make inspect-sdk
```

To change only the public constructor's device argument while preserving the
rest of the probe:

```bash
make inspect-sdk-cpu
```

The default target preserves the original automatic-device failure for
comparison. The CPU target tests whether avoiding automatic device mapping
also avoids the `accelerate` requirement.

The Makefile ensures that:

- Python packages come from `/tmp/call-me-maybe-venv`;
- package downloads use `/tmp/call-me-maybe-uv-cache`;
- Hugging Face model/tokenizer files use
  `/tmp/call-me-maybe-huggingface`.

`inspect_sdk.py` uses only public `Small_LLM_Model` methods. It records:

- model construction time;
- encoded token IDs, shape, dtype, and device;
- direct and unbatched decode behavior;
- public tokenizer-file paths;
- logits count and computation time;
- the highest-scoring next-token candidates.

The corresponding findings belong in a numbered learning waypoint. Do not
turn this experiment into production code.

The default probe reproduced a device-map requirement for `accelerate`.
The controlled CPU probe succeeded:

```bash
make inspect-sdk-cpu
```

Its results are recorded in Waypoint 007.
