# Runtime Flow: Variable Ledger and Discussion

- Kind: Thematic talking point
- Theme: LLM SDK and `inspect_sdk`
- Depth: Detailed reference and question-led discussion
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: [Runtime-flow map](index.md)

## Complete variable ledger

### Probe module and helpers

| Name | Owner/scope | Type | Recorded or typical value |
|---|---|---|---|
| `PROMPT` | module | `str` | `What is the sum of 2 and 3?` |
| `TOP_CANDIDATE_COUNT` | module | `int` | `10` |
| `parser` | `parse_device_argument` | `ArgumentParser` | command-line rules object |
| `requested_device` | `main` | `str | None` | `"cpu"` in controlled run |
| `title` | `print_heading` | `str` | current section name |
| `construction_started` | `main` | `float` | monotonic counter reading |
| `model` | `main` | `Small_LLM_Model` | initialized wrapper instance |
| `construction_seconds` | `main` | `float` | observed `18.419` |
| `encoded` | `main` | `torch.Tensor` | shape `(1, 11)`, CPU, int64 |
| `input_ids` | `main` | `list[int]` | 11 prompt token IDs |
| `direct_decoded` | `main` | observed `list[str]` | one-element text batch |
| `row_decoded` | `main` | `str` | original prompt text |
| `label` | file helper | `str` | vocabulary/merges/tokenizer |
| `path_getter` | file helper | `Callable[[], str]` | bound SDK method |
| `path` | file helper | `Path` | cached artifact path |
| `error` | exception block | `Exception` | only present on failure |
| `logits_started` | `main` | `float` | counter before forward pass |
| `logits` | `main` | `list[float]` | length 151,936 |
| `logits_seconds` | `main` | `float` | observed `0.301` |
| `top_token_ids` | `main` | `list[int]` | ten highest score indices |
| `rank` | loop | `int` | 1 through 10 |
| `token_id` | loop | `int` | one selected vocabulary ID |
| `token_text` | loop | `str` | decoded one-token fragment |

### SDK constructor and state

| Name | Owner/scope | Type | Role |
|---|---|---|---|
| `self` | every SDK method | `Small_LLM_Model` | current wrapper instance |
| `model_name` | constructor | `str` | model repository ID |
| `device` | constructor local | `str | None` then `str` | chosen backend |
| `dtype` | constructor local | `torch.dtype | None` then dtype | precision |
| `trust_remote_code` | constructor | `bool` | loading permission flag |
| `self._model_name` | instance | `str` | retained repository ID |
| `self._device` | instance | `str` | retained computation backend |
| `self._dtype` | instance | `torch.dtype` | retained precision |
| `self._tokenizer` | instance | tokenizer object | text/ID translation and file metadata |
| `self._model` | instance | causal LM object | forward inference |
| `p` | constructor loop | `torch.nn.Parameter` | one model parameter |

### SDK method locals

| Name | Method | Type/shape | Role |
|---|---|---|---|
| `text` | `encode` | `str` | input text |
| `ids` | `encode` | `list[int]` | tokenizer output |
| `ids` | `decode` | tensor then list | IDs being decoded |
| `input_ids` | logits method | `list[int]` | prompt sequence |
| `input_tensor` | logits method | Tensor `(1, sequence_length)` | batched model input |
| `out` | logits method | model output object | contains full logits tensor |
| `logits` | logits method | `list[number]` | final-position scores before float normalization |
| `vocab_file_name` | vocab getter | `str` | remote/cached artifact filename |
| `vocab_path` | vocab getter | `str` | local path returned by hub helper |
| `merges_file_name` | merges getter | `str` | artifact filename |
| `merges_path` | merges getter | `str` | local cache path |
| `tokenizer_file_name` | tokenizer getter | `str` | artifact filename |
| `tokenizer_path` | tokenizer getter | `str` | local cache path |

## Function contract guide

| Function/method | Receives | Returns | Important side effect |
|---|---|---|---|
| `parse_device_argument` | process arguments implicitly | `str | None` | may terminate on invalid CLI input |
| `print_heading` | title string | `None` | prints text |
| `inspect_tokenizer_file` | label and bound getter | `None` | may download/check/print file data |
| `Small_LLM_Model.__init__` | configuration | implicit `None` | loads and stores tokenizer/model |
| `encode` | text | 2-D tensor | none beyond computation |
| `decode` | tensor or ID list | annotated `str`; batched result differs | none beyond computation |
| `get_logits_from_input_ids` | one ID sequence | vocabulary-sized float list | performs model forward pass |
| tokenizer file getters | none beyond bound `self` | path string | may retrieve/cache an artifact |
| `main` | nothing explicit | `None` | coordinates the entire report |

## Call boundary questions for voice discussion

At each arrow, ask what changes representation:

```text
shell text --argparse--> Python string
Python string --tokenizer--> list[int]
list[int] --torch.tensor--> 2-D integer tensor
tensor --model--> 3-D logits tensor inside output object
3-D tensor --indexing--> 1-D vocabulary-score tensor
tensor --tolist/float--> list[float]
score indices --tokenizer.decode--> strings
path strings --Path--> filesystem helper objects
```

Recommended questions:

- Which transformations copy data, and which only select/view it?
- Why does the model require a batch dimension?
- Why are input IDs integers but model logits floating-point values?
- Which values remain on the SDK object between method calls?
- Which variables disappear after a helper returns?
- Why is `model` constructed once and reused?
- At which exact line does neural inference happen?
- Why does `[0, -1]` represent the next-token decision?
- Why can the logit index be treated as a token ID?
- Which operations might download files?
- Which source members are public, and which are private?
- What would change in the variable ledger for two prompts in one batch?

## Source facts versus recorded observations

### Guaranteed by the current source path

- The probe uses only public SDK methods.
- Explicit `--device cpu` passes `"cpu"` to the constructor.
- `encode()` wraps tokenizer IDs in one batch dimension.
- token IDs use `torch.long`.
- the logits method selects batch zero and final sequence position.
- the probe ranks exactly ten IDs unless the constant changes.

### Observed in the recorded CPU run

- construction succeeded in 18.419 seconds;
- the prompt became 11 IDs;
- the tensor was on CPU with shape `(1, 11)`;
- batched decode returned `list[str]`;
- row decode returned `str`;
- all three tokenizer files existed;
- the logits list contained 151,936 floats;
- one logits calculation took 0.301 seconds;
- the highest candidates were ordinary prose fragments.

### Still open or intentionally untested

- whether automatic device selection should be repaired for production;
- whether `accelerate` should be declared;
- how CUDA timing compares on evaluator hardware;
- the final prompt format for semantic function selection;
- complete token-by-token generation;
- constrained JSON decoding;
- Pydantic validation of generated calls.

## Common misconceptions

- Importing a class does not construct its model.
- Calling a class returns an instance even though `__init__()` itself returns
  `None`.
- `_model` and `_tokenizer` can be explained without being permitted in
  application code.
- A tensor is an object containing numerical data plus shape, dtype, and
  device metadata; it is not merely a Python list.
- Batch size one is still a batch dimension.
- Token IDs are vocabulary indices, not character codes.
- Logits are scores, not generated text and not probabilities.
- One logits vector represents one next-token decision, not a full response.
- `hf_hub_download` may return a cached path without transferring the file
  again.
- A variable name does not “contain the type”; it refers to an object whose
  runtime type and current value can be inspected.
- Type annotations guide humans and tools but do not always enforce runtime
  behavior, as the batched decode result demonstrates.

## Successful discussion outcome

The learner should be able to narrate the entire execution without reading
line by line, then zoom into any boundary and state:

1. which layer is running;
2. which function or method owns control;
3. which variables exist;
4. their types, shapes, and representative values;
5. what object is returned;
6. what persists after the call;
7. whether the claim comes from source, observation, requirement, or
   interpretation.

## Linked sources

- [LLM-SDK theme home](../index.md)
- [Runtime-flow map](index.md)
- [`experiments/inspect_sdk.py`](../../../../../../experiments/inspect_sdk.py)
- [`Small_LLM_Model` source](../../../../../../llm_sdk/llm_sdk/__init__.py)
- [Makefile](../../../../../../Makefile)
- [SDK reference](../../../../../reference/llm-sdk.md)
- [`inspect_sdk.py` probe overview](../probe/index.md)
- [Waypoint 006: first SDK probe](../../../../waypoints/006-2026-11-10-first-sdk-probe.md)
- [Waypoint 007: explicit-CPU probe](../../../../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md)
- [Waypoint 008: editor navigation](../../../../waypoints/008-2026-11-12-editor-navigation-and-environment-storage.md)

## Update log

| Date | Change |
|---|---|
| 2026-11-13 | Created the full Make-to-model execution walkthrough, variable ledger, class-state explanation, call contracts, evidence labels, and maintenance rules. |
