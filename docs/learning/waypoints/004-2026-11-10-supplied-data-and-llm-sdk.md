# Waypoint 004: Supplied Data and LLM SDK

Date: 2026-11-10  
Stage: Concept and interface study  
Status: In progress

## Purpose

Understand the supplied JSON files and SDK before designing or implementing
the application.

## Topics covered

- Prompt and function-definition formats.
- Semantic function selection versus keyword heuristics.
- Python dependency resolution.
- Runtime model download.
- Token IDs, tensors, logits, and vocabulary files.
- Public versus private SDK interfaces.
- Device and dtype selection.
- Constrained next-token selection.

## Progress made

- Inspected both supplied JSON files.
- Inspected `llm_sdk/llm_sdk/__init__.py` method by method.
- Answered the learner's questions in the original learning-plan draft.
- Added `docs/reference/llm-sdk.md`.
- Added `docs/reference/imports.md`.
- Replaced SDK TODO notes with concise explanatory comments.
- Removed three unused SDK imports rather than pretending they were required.
- Ran an import-only SDK experiment.
- Created open-question and issue registers.

## Questions and answers

### Where is the LLM? Does `uv` install it?

The LLM is the model identified by `Qwen/Qwen3-0.6B`, the constructor's
default `model_name`.

`uv sync` installs the Python libraries used to run the model: the local SDK,
PyTorch, Transformers, and Hugging Face Hub. It does not install the Qwen
weights into the environment. Constructing `Small_LLM_Model()` calls
`from_pretrained(...)`; those calls download and cache the tokenizer and
model files if they are absent.

Because the home partition is small, model experiments should use a cache on
the larger filesystem, for example:

```bash
HF_HOME=/tmp/call-me-maybe-huggingface uv run python ...
```

### Where is `Small_LLM_Model` invoked?

Nowhere yet. The SDK file defines a class; definitions do not construct
objects automatically. Future application or experiment code must import and
instantiate it:

```python
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
```

### What does constrained decoding control?

The LLM returns a score for every possible next token. The decoder determines
which of those tokens would preserve valid JSON and the required schema.
Invalid candidates receive a logit of negative infinity, making them
unselectable.

For example, after:

```text
{"name":
```

a token beginning an allowed quoted function name may be valid, while `]`
cannot be valid in that position. The LLM still ranks the valid choices; the
decoder supplies the structural boundary.

### How are prompts represented?

`function_calling_tests.json` is a JSON array. Each element is an object whose
`prompt` key contains the natural-language request as a string.

### How are functions represented?

`functions_definition.json` is a JSON array of function objects. Each object
contains:

- `name`;
- `description`;
- `parameters`;
- `returns`.

`parameters` is an object mapping semantic parameter names such as `a`,
`name`, `source_string`, and `regex` to type schemas.

### Which JSON types currently appear?

At the file-structure level, the examples use arrays, objects, and strings. At
the function-schema level, the current declared value types are `string` and
`number`. The subject mentions other types, including `boolean`, and
evaluation data may differ.

### Does function selection use keywords such as “sum” or “add”?

Not in application rules. The prompt and available function descriptions are
given to the language model, whose learned semantics should make the suitable
function name more likely.

The model can treat words such as “sum” as evidence, but project code may not
implement a rule such as:

```python
if "sum" in prompt:
    choose("fn_add_numbers")
```

Constrained decoding may restrict output to the available function names, but
the relative semantic choice must come from model scores.

### What does `encode()` return?

It asks the tokenizer to convert text into integer token IDs, then returns a
PyTorch tensor shaped:

```text
[1, token_count]
```

The first dimension is a batch containing one sequence. Values use
`torch.long` because token IDs are integers. The tensor is created on the
selected CPU, CUDA, or MPS device.

If text becomes token IDs `[42, 105, 9]`, the result is conceptually:

```text
[[42, 105, 9]]
```

### What does `decode()` accept?

Its annotation accepts either a `torch.Tensor` or `list[int]`. Tensor input is
converted to a Python list before the tokenizer reconstructs text.

An unresolved interface question remains: `encode()` returns a 2-D tensor,
while tokenizer decode normally expects a 1-D sequence. We need to compare
`decode(encoded)` with `decode(encoded[0])`. This is `Q-001`.

### What is a token?

A token is one vocabulary unit used by the model. It is not necessarily one
character or one word. It may be:

- a complete common word;
- part of a word;
- punctuation;
- whitespace plus following text;
- an encoded byte or Unicode fragment.

Multiple-character tokens represent frequent text efficiently, while smaller
pieces allow uncommon words to be composed without an unlimited vocabulary.

### What is a logit?

A logit is an unnormalized score for one possible next token. A larger logit
means the model considers that token more plausible in the current context.
Softmax could convert all logits into probabilities, but masking and ranking
can operate directly on raw logits.

### What shape does `get_logits_from_input_ids()` return?

The model initially returns:

```text
[batch_size, sequence_length, vocabulary_size]
```

The SDK selects `out.logits[0, -1]`: the first batch item and final input
position. It returns that as a one-dimensional `list[float]` of length
`vocabulary_size`. Index `i` is the score for token ID `i`.

### How does generation continue after selecting a token?

Append the selected token ID to the existing input-ID sequence. Submit the
longer sequence for the next logits call. Each prediction therefore depends
on the prompt and all previously generated tokens; this is autoregressive
generation.

### Where is the vocabulary file?

It belongs to the selected Hugging Face model and is not committed to this
repository. The SDK's path methods download vocabulary, merges, or complete
tokenizer files into the Hugging Face cache and return their local paths.

Their exact availability and format must be inspected at runtime. This is
tracked as `Q-003`.

### Which SDK methods are public?

The usable public interface is:

- `Small_LLM_Model(...)`;
- `encode(...)`;
- `decode(...)`;
- `get_logits_from_input_ids(...)`;
- `get_path_to_vocab_file()`;
- `get_path_to_merges_file()`;
- `get_path_to_tokenizer_file()`.

The subject forbids direct access to underscore-prefixed attributes and
methods.

### What internal state does the SDK manage?

| Attribute | Meaning |
|---|---|
| `_model_name` | Hugging Face repository identifier. |
| `_device` | CPU, CUDA, or MPS computation location. |
| `_dtype` | Model numeric precision. |
| `_tokenizer` | Text/token conversion implementation. |
| `_model` | Loaded causal language model. |

These are private implementation details even though Python does not enforce
privacy at the language level.

### What do device and dtype mean?

The device says where computation and tensors live:

- `cpu`: processor and normal system memory;
- `cuda`: NVIDIA GPU;
- `mps`: Apple GPU backend.

The dtype says how model numbers are represented. `float16` uses less memory
and is suited to supported accelerators. `float32` uses more memory but has
broader CPU compatibility. The SDK stores both choices so the model and input
tensors remain compatible.

### How are Python imports resolved?

`uv run` uses the project's selected Python environment. Python searches its
`sys.path`, including standard-library locations and the environment's
`site-packages`. The root `pyproject.toml` tells `uv` that `llm-sdk` comes
from the local `llm_sdk/` directory; the SDK's third-party dependencies come
from the resolved package graph.

An editor can navigate to imported source only when its language server is
using the correct project interpreter and the dependency is installed.

## Evidence and experiments

### Import-only experiment

The SDK was imported without constructing a model, so no model download was
requested.

Result:

```text
ModuleNotFoundError: No module named 'transformers'
```

Package inspection showed that `.venv` contains PyTorch, Hugging Face Hub,
tokenizers, and the local SDK, but not Transformers. The environment is not
fully synchronized with the current lockfile. This is issue `I-001`.

### Targeted Flake8 check

The SDK file compiles, but a targeted Flake8 run reports pre-existing long
lines and extra blank lines. This is issue `I-002`.

## Decisions

- Do not begin application implementation until the supplied interfaces are
  understood.
- Keep semantic function choice and structural token filtering conceptually
  separate.
- Use only public SDK methods.
- Store durable SDK explanations in reference documents.
- Track experiments that still need evidence as open questions rather than
  presenting assumptions as facts.
- Keep model cache data off the constrained home filesystem during local
  experiments.

## Open questions or issues

- `Q-001`: direct encode/decode round trip.
- `Q-002`: complete mandatory parameter-type set.
- `Q-003`: actual Qwen tokenizer files.
- `Q-004`: prompt format for reliable function selection.
- `Q-005`: representation of per-prompt failure.
- `I-001`: incomplete project environment.
- `I-002`: SDK Flake8 failures.

## Documents created or updated

- `docs/reference/llm-sdk.md`
- `docs/reference/imports.md`
- `docs/project/questions.md`
- `docs/project/issues.md`
- `llm_sdk/llm_sdk/__init__.py`
- `docs/index.md`

The original combined learning plan and annotations were preserved as
`docs/archive/learning-plan-and-questions-draft.md`.

## Next step

Review these explanations, fully synchronize the environment, and then run
small public-interface experiments before designing application architecture.
