# Living Talking Points: Full `inspect_sdk` Flow

- Kind: Thematic talking point
- Theme: LLM SDK and `inspect_sdk`
- Depth: Detailed execution flow
- Status: Living
- First created: 2026-11-13
- Last reviewed: 2026-11-13
- Primary probe: `experiments/inspect_sdk.py`
- Supplied implementation: `llm_sdk/llm_sdk/__init__.py`

This document follows the complete execution path of the SDK probe. It is
intended to be expanded whenever the learner adds a question, a new branch is
tested, or runtime evidence changes.

It complements the [`inspect_sdk.py` agent briefing](../probe/index.md):

- the agent briefing emphasizes provenance, experiment design, results, and
  likely questions;
- this guide emphasizes control flow, call boundaries, variables, types,
  shapes, object state, and what every layer is holding at each moment.

## Suggested instruction for a voice agent

> Read `docs/learning/talking-points/themes/llm-sdk/runtime-flow/index.md`,
> `experiments/inspect_sdk.py`, and `llm_sdk/llm_sdk/__init__.py`. Walk through
> the program from the Make target to process exit. At every step, ask me what
> executes next, which function owns each variable, its type and current value
> or shape, and what crosses into or returns from the SDK. Let me answer first,
> then correct or extend my explanation. Distinguish source-code facts,
> runtime observations, requirements, and unresolved questions. Do not move to
> application implementation unless I explicitly ask.

## Maintenance rules

When this guide is updated:

1. Preserve earlier observed results unless a later run disproves them.
2. Label claims as one of:
   - **source fact**: visible directly in the code;
   - **observed fact**: measured during a recorded run;
   - **requirement**: imposed by the project subject;
   - **interpretation**: a reasoned explanation;
   - **open question**: not yet established.
3. Add learner questions beneath the stage where they arise.
4. Update the variable ledger when a variable or return shape changes.
5. Keep production design separate from diagnostic behavior.
6. Add a dated entry to the update log at the end.

## The four layers

The word “program” can hide several separate systems:

```text
Layer 1: Make and uv
    choose a saved command and prepare the Python environment

Layer 2: experiments/inspect_sdk.py
    coordinate and report the diagnostic experiment

Layer 3: Small_LLM_Model in the supplied SDK
    wrap tokenizer/model loading and public inference operations

Layer 4: PyTorch, Transformers, Hugging Face, and Qwen
    implement tensors, tokenization, model inference, and cached artifacts
```

The probe may call a one-line SDK method that performs many operations in the
underlying libraries. A useful discussion should always identify which layer
currently owns the behavior.

## Whole-flow map

```text
make inspect-sdk-cpu
    |
    v
Make exports /tmp paths
    |
    v
uv run python experiments/inspect_sdk.py --device cpu
    |
    v
Python imports probe dependencies and defines functions/constants
    |
    v
module guard calls main()
    |
    +--> parse_device_argument() ----------------------> "cpu"
    |
    +--> Small_LLM_Model(device="cpu")
    |       |
    |       +--> choose device and dtype
    |       +--> load tokenizer
    |       +--> load causal language model
    |       +--> move model to CPU
    |       +--> evaluation mode; gradients disabled
    |       '--> constructed SDK object
    |
    +--> model.encode(PROMPT) -------------------------> Tensor (1, 11)
    |       '--> tokenizer text -> token IDs
    |
    +--> encoded[0].tolist() --------------------------> list[int], length 11
    |
    +--> model.decode(encoded) ------------------------> observed list[str]
    +--> model.decode(encoded[0]) ---------------------> observed str
    |
    +--> public tokenizer-file getters
    |       '--> Hugging Face cache path strings
    |
    +--> model.get_logits_from_input_ids(input_ids)
    |       +--> list -> Tensor (1, 11)
    |       +--> model forward pass
    |       +--> output logits (1, 11, 151936)
    |       +--> select [batch 0, final position]
    |       '--> list[float], length 151936
    |
    +--> nlargest(...) --------------------------------> ten token IDs
    +--> decode each one-token candidate --------------> readable fragments
    |
    v
main() returns; Python process exits; in-memory model is released
```

## Choose a stage

1. [Command, environment, module entry, and arguments](command-and-entry.md)
2. [`Small_LLM_Model` construction](model-construction.md)
3. [Encoding and decoding](encoding-and-decoding.md)
4. [Tokenizer files](tokenizer-files.md)
5. [Logits and candidate ranking](logits-and-ranking.md)
6. [Variable ledger, contracts, evidence, and discussion](variable-ledger-and-discussion.md)

## Related learning

- [LLM-SDK theme home](../index.md)
- [Probe overview](../probe/index.md)
- [`inspect_sdk.py`](../../../../../../experiments/inspect_sdk.py)
- [`Small_LLM_Model` source](../../../../../../llm_sdk/llm_sdk/__init__.py)

