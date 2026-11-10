# Learning Experiments

These programs investigate supplied components before production design begins.
They are evidence-generating tools, not application implementation.

## SDK probe

Run:

```bash
make inspect-sdk
```

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
