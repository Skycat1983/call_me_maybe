# Probe Questions and Discussion

- Kind: Thematic talking point
- Theme: LLM SDK and `inspect_sdk`
- Depth: Question-led discussion
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: [Probe overview](index.md)

## Common questions and concise answers

### Did we create this file or download it?

We created it locally with AI assistance. Its docstring, experiment README,
and Waypoint 007 record that provenance.

### Was it generated automatically?

No tool generated it as a project artifact. The assistant authored the code
from a human-readable experiment plan based on the SDK's public methods. The
runtime values were then obtained by executing that code.

### How did the assistant know what to put in it?

By mapping each unresolved question to the smallest public method call that
could produce evidence, then adding standard-library code to time, display,
and compare the results.

### What is `__doc__`?

It is the special attribute through which Python exposes the docstring of the
current module, class, or function. At module level in this file, `__doc__`
contains the explanatory string at the very top of `inspect_sdk.py`. The
script passes it to `ArgumentParser` so that text appears in `--help` output.

### What does “optional public SDK device override” mean?

The command may omit `--device`, in which case the SDK selects automatically,
or provide one documented device value to replace that automatic choice for
the run. The explicit CPU override gave us a controlled way to test whether
the earlier failure belonged to automatic device mapping.

### What are device arguments, and why are they useful?

They are command-line values selecting the computation backend: CPU, an
NVIDIA GPU through CUDA, or Apple's GPU through MPS. They let the same probe
choose hardware without editing its source and let experiments compare device
paths explicitly.

### Why does `--device` use these parser arguments?

The option name mirrors the SDK constructor's `device` parameter; `choices`
limits input to the constructor's CPU, CUDA, and MPS values; and `help`
explains the option in the generated help screen. Omitting a default
intentionally produces `None`, preserving automatic selection when the option
is not used.

### How should I know that a tensor has `.tolist()`?

You are not supposed to know every library method in advance. Start from the
return annotation: `encode()` says it returns `torch.Tensor`. Hover over the
variable, type `encoded.`, use Ctrl+click/F12, inspect the library help, or
consult its documentation. Those tools reveal `.tolist()` and explain that it
converts tensor values into ordinary Python lists.

### Why convert `encoded.shape` to a tuple?

Only to make the diagnostic output read `(1, 11)` instead of
`torch.Size([1, 11])`. Both carry the same dimensions; the tuple is a simpler
display value and is not required by the model.

### What exactly does Make do here?

It finds the named target and executes its stored shell recipe. The recipe
runs Python through `uv`; Python, not Make, performs the SDK calls.

### How do we know it genuinely ran?

The real run produced model-loading activity, elapsed timings, tensor data,
decoded return values, file sizes, 151,936 model scores, candidate texts, and
exit code `0`. A dry run could produce none of those runtime facts.

### Why use explicit CPU?

It changed one constructor value after the automatic path failed. The result
isolated a working path without immediately changing dependencies, making the
experiment easier to interpret.

### Why not just install `accelerate`?

Installing it might make the automatic device-map path proceed, but that
would change a second variable before learning whether the public CPU option
already worked. The CPU test answered that narrower question first. GPU and
automatic-device requirements remain a separate decision.

### Are logits probabilities?

No. They are raw model scores. A softmax operation can transform a vector of
logits into probabilities, but this probe does not need probabilities to rank
the candidates because softmax preserves their order.

### Why does `nlargest` receive indices rather than logits directly?

The program needs token IDs after ranking. Ranking the indices with their
associated scores preserves each score's position, and that position is the
token ID used by `decode()`.

### Why decode both `encoded` and `encoded[0]`?

To test whether the wrapper handles a batch and a single sequence in the same
way. The differing container types exposed a useful interface inconsistency.

### Why are some failures caught while construction is not?

Decode forms and file getters are independent diagnostic checks, so the probe
can report one failure and continue gathering evidence. Construction and
logits are central milestones; if either fails, a nonzero exit and traceback
make the incomplete run unmistakable.

### Why did the top candidates not answer `5`?

The printed candidates are the model's very next token after a bare question,
not a complete generated answer. The wrapper also did not apply a chat
template or instruction to answer directly. A full answer would require a
generation loop that repeatedly chooses and appends tokens.

### Does the probe modify project data?

It does not modify source or input data. It may create or refill the external
Python and Hugging Face caches required to run the model.

## Likely misconceptions to correct

- `make -n` is not evidence that the Python program ran.
- A successful CPU run does not mean the automatic-device failure is fixed.
- `(1, 11)` means one sequence of eleven tokens, not eleven independent
  prompts.
- Token IDs are vocabulary references, not Unicode character codes.
- The logit count is vocabulary size, not prompt length.
- One logit vector represents one next-token decision, not a generated reply.
- The top candidate is not automatically the candidate that must be chosen;
  later decoding policy may sample or apply constraints.
- A model cannot select among project functions that have never been
  described in its input.
- A 0.301-second forward pass is not a full end-to-end application benchmark.
- Diagnostic exception handling should not automatically be copied into
  production code.

## Good follow-up discussion questions

1. Which statements in this document come from source inspection, and which
   required a real run?
2. Why is the CPU comparison stronger evidence than changing the dependency
   list and device behavior simultaneously?
3. How do batch dimension and sequence dimension explain the two decode
   return values?
4. Why can token IDs double as indices into the logits vector?
5. What additional context must a function-calling prompt contain?
6. What would a generation loop need to do after receiving the first logits
   vector?
7. At what stage should constrained decoding limit allowed next tokens?
8. Where should Pydantic validation occur, and what would it validate?
9. Which parts of this probe are reusable diagnostics, and which are specific
   to this one learning question?
10. What evidence would be needed before deciding to add `accelerate`?

## Guidance for the discussing agent

- Lead with an explanation, then ask the learner to restate it in their own
  words.
- Use the actual values above when explaining tensors, decode types, and
  logits.
- Label source facts, observed facts, hypotheses, and open decisions.
- Do not present the probe as production code or as completed function
  calling.
- Do not imply that automatic/GPU loading was repaired.
- If proposing a next experiment, explain its question, controlled variable,
  expected evidence, and failure interpretation before writing code.

## Recommended next conceptual step

Before implementing constrained generation, design the smallest prompt that
teaches the model the available function names, descriptions, parameter
schemas, and required output shape. Then run another controlled probe to see
whether the model's next-token scores begin to reflect that information.

That future experiment should remain separate from `inspect_sdk.py` so this
file continues to document the basic public SDK behavior already observed.

## Quick glossary

| Term | Meaning here |
|---|---|
| token | A model vocabulary unit; it may be a word, fragment, space, punctuation, or another text piece |
| token ID | The integer position identifying a token in the vocabulary |
| tensor | PyTorch's multidimensional numeric data container |
| batch | A group of sequences processed together; this probe has a batch size of one |
| sequence length | Number of token IDs in one encoded input |
| decode | Convert token IDs back into text |
| logit | A raw score for a possible next token |
| forward pass | Run input through the model once to obtain output scores |
| vocabulary size | Number of token IDs the model can score; observed here as 151,936 |
| device | Hardware/backend used for tensor computation, such as CPU or CUDA |
| cache | Re-downloadable local data used to avoid repeated package or model downloads |
| controlled experiment | A comparison intended to change one relevant variable at a time |

## Repository references

- [LLM-SDK theme home](../index.md)
- [Probe overview](index.md)
- [`experiments/inspect_sdk.py`](../../../../../../experiments/inspect_sdk.py)
- [experiment README](../../../../../../experiments/README.md)
- [Makefile](../../../../../../Makefile)
- [Waypoint 006: first SDK probe](../../../../waypoints/006-2026-11-10-first-sdk-probe.md)
- [Waypoint 007: explicit-CPU SDK probe](../../../../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md)
- [LLM SDK reference](../../../../../reference/llm-sdk.md)
- [project questions](../../../../../project/questions.md)
- [known issues](../../../../../project/issues.md)
