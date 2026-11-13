# Probe Source Walkthrough

- Kind: Thematic talking point
- Theme: LLM SDK and `inspect_sdk`
- Depth: Applied code walkthrough
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: [Probe overview](index.md)

## Source walkthrough

### Imports

`ArgumentParser` implements the optional `--device` command-line argument.
The allowed values are `cpu`, `cuda`, and `mps`.

`Callable` describes the type of the public path-getter functions passed to
`inspect_tokenizer_file()`.

`nlargest` selects the indices with the highest corresponding logit values.
It avoids sorting every score when only ten results are needed.

`Path` converts each returned path string into an object that can check
whether the file exists and query its size.

`perf_counter` measures elapsed construction and forward-pass time. It is
appropriate for durations; it is not being used as a calendar clock.

`cast` tells Mypy the expected static type of a value when a library API is
too dynamic for the checker to infer it. It does not convert, validate, or
otherwise change the value at runtime.

`Small_LLM_Model` is the supplied wrapper being investigated. The experiment
does not reach into its private fields.

### Constants

```python
PROMPT = "What is the sum of 2 and 3?"
TOP_CANDIDATE_COUNT = 10
```

The prompt is intentionally simple. At this stage the goal was to observe the
SDK mechanics, not to test function-calling quality. Ten candidates provide a
small readable sample of the logits vector.

### `parse_device_argument()`

This helper defines and parses `--device`. If the option is absent, it returns
`None`; that value is passed to the SDK's automatic device path. With
`--device cpu`, it returns `"cpu"` and changes only the constructor argument.

The parser is constructed with:

```python
ArgumentParser(description=__doc__)
```

`__doc__` is a special Python module attribute. Because this file begins with
a triple-quoted module docstring, Python stores that string in `__doc__` while
the module is loaded. Passing it as the parser description means
`python experiments/inspect_sdk.py --help` displays the same description. It
avoids maintaining a second copy of that explanatory text. If a module has no
docstring, its `__doc__` value is normally `None`, which `ArgumentParser` also
accepts.

The following `add_argument()` call defines one optional command-line input:

```python
parser.add_argument(
    "--device",
    choices=("cpu", "cuda", "mps"),
    help="Pass an explicit device to Small_LLM_Model.",
)
```

Those arguments were chosen for distinct reasons:

- `"--device"` gives the option its command-line spelling. The leading two
  hyphens make it optional, so the probe can still exercise automatic device
  selection when the option is omitted.
- `choices=("cpu", "cuda", "mps")` restricts input to the three device names
  accepted by the supplied SDK's public constructor: ordinary processor,
  NVIDIA CUDA GPU, or Apple's Metal backend. `argparse` rejects a typo or an
  unsupported value before model construction begins.
- `help=...` provides the short explanation shown beside the option in
  `--help` output.

No `type=` is required because command-line values are strings by default. No
`default=` is required because an omitted optional argument defaults to
`None`, which is precisely what the experiment needs to retain the SDK's
automatic-selection path. Finally, `.parse_args().device` returns the value
stored under the name inferred from `--device`.

The function returns it through:

```python
return cast(str | None, parser.parse_args().device)
```

`ArgumentParser` creates a `Namespace` whose attributes depend on calls to
`add_argument()`. Mypy therefore sees `.device` as `Any`, even though the
parser rules prove that this script receives a permitted string or `None`.
`cast` records that fact for static analysis. It emits no runtime check; the
parser's `choices` and omitted-option behavior remain the runtime controls.

The function docstring says it returns an “optional public SDK device
override.” “Optional” means the caller does not have to provide it. “Public
SDK” means the value is passed through the documented constructor parameter,
not written into a private field. “Override” means an explicit choice replaces
automatic device selection for that run. This is useful for predictable
hardware selection and, here, for isolating one variable after the automatic
path failed.

That single-variable change is important: it makes the default and CPU runs
useful as a controlled comparison.

### `print_heading(title)`

This helper only makes terminal output easier to scan. It has no effect on
model behavior.

### `inspect_tokenizer_file(label, path_getter)`

This helper accepts a label and one bound public SDK method. It:

1. calls the method to get a path string;
2. creates a `Path` object;
3. prints the path;
4. reports whether it is a file;
5. prints its size when present.

The local `try`/`except` lets the probe report one failed path method and then
continue checking the others. Catching `Exception` broadly would generally be
too permissive in production code, but here the purpose is to collect
diagnostic evidence from independent checks.

### `main()`

`main()` coordinates the experiment in five sections.

#### 1. Model construction

It parses the device, starts a timer, calls:

```python
model = Small_LLM_Model(device=requested_device)
```

and reports elapsed time. Construction errors are deliberately not caught.
If the model cannot load, Python prints the traceback and exits unsuccessfully
instead of allowing later output to imply that the full experiment succeeded.

The printed Qwen identifier documents the model expected from the supplied
wrapper. It does not itself select or configure the model.

#### 2. Encoding

```python
encoded = model.encode(PROMPT)
input_ids = encoded[0].tolist()
```

`encoded` is the SDK's tensor result. Indexing with `[0]` selects the first
sequence from the batch. Calling `.tolist()` converts that one-dimensional
tensor to the ordinary Python `list[int]` expected by
`get_logits_from_input_ids()`.

The learner is not expected to guess or memorize that `.tolist()` exists.
There are several discoverable sources of that information:

- `Small_LLM_Model.encode()` declares its return type as `torch.Tensor`;
- hovering over `encoded` lets Pylance use that annotation to show the type;
- typing `encoded.` lets IntelliSense suggest tensor members;
- Ctrl+click or F12 can navigate into available type/source information;
- Python can display `help(torch.Tensor.tolist)` at runtime;
- PyTorch's installed `_tensor_docs.py` documents the method.

The installed method describes itself as converting a tensor to a nested
Python list, or a Python number for a scalar. In this probe, `encoded[0]` is
one-dimensional, so `.tolist()` produces a flat `list[int]` of token IDs.

The shape is printed as `tuple(encoded.shape)` only for concise output.
`encoded.shape` is already an iterable `torch.Size` object and would contain
the same dimensions, but it displays as `torch.Size([1, 11])`. Converting it
to a tuple displays `(1, 11)`, making the batch and sequence dimensions easier
to read and less tied to PyTorch. The conversion is not required for model
operation.

The program prints the prompt, tensor shape, dtype, device, token count, and
IDs so none of those properties need to be guessed.

#### 3. Decoding

The probe intentionally calls decode in two ways:

```python
model.decode(encoded)
model.decode(encoded[0])
```

Both calls are wrapped separately so that failure of the first form would not
prevent testing the second. The comparison investigates dimensionality:
`encoded` is a batch containing one sequence, while `encoded[0]` is the one
sequence itself.

#### 4. Tokenizer files

The three calls use the public getters:

- `get_path_to_vocab_file`;
- `get_path_to_merges_file`;
- `get_path_to_tokenizer_file`.

Passing these bound methods as values lets one helper perform the same
existence-and-size check for each without duplicating code.

#### 5. Next-token logits

```python
logits = model.get_logits_from_input_ids(input_ids)
```

This performs one model forward pass and returns a score for each possible
next token. These values are logits: raw comparative scores, not normalized
probabilities. A larger logit means the token is preferred relative to a
lower-scoring token in that position.

The selection code is:

```python
top_token_ids = nlargest(
    TOP_CANDIDATE_COUNT,
    range(len(logits)),
    key=logits.__getitem__,
)
```

`range(len(logits))` produces all possible indices. Here each index is also a
token ID. `key=logits.__getitem__` tells `nlargest` to compare those IDs using
the score stored at each index. The result is therefore the ten token IDs with
the highest scores, in descending order.

Each selected ID is passed as a one-item list to `decode()` so the terminal
can show both its numeric score and readable token text.

The logits call and candidate decodes are not caught. A failure makes the
experiment exit unsuccessfully, which is appropriate because they are central
to the result rather than optional metadata checks.

### Module guard

```python
if __name__ == "__main__":
    main()
```

When Python executes this file directly, `__name__` is `"__main__"`, so the
experiment runs. If another module imports the file, its functions and
constants become available without automatically loading the model.

## Data flow

```text
plain-text prompt
    -> model.encode(...)
    -> 2-D integer tensor: one batch x eleven tokens
    -> encoded[0]
    -> 1-D sequence tensor
    -> .tolist()
    -> list of integer token IDs
    -> model.get_logits_from_input_ids(...)
    -> 151,936 raw next-token scores
    -> select ten largest score indices
    -> decode each selected token ID
    -> readable candidate token fragments
```

Encoding and logits answer different questions. Encoding asks, “How is the
existing prompt represented?” Logits ask, “Given that prompt, how strongly
does the model score each possible next token?”

## Related learning

- [LLM-SDK theme home](../index.md)
- [Probe overview](index.md)
- [Experiments and results](experiments-and-results.md)
- [Detailed runtime flow](../runtime-flow/index.md)
- [`inspect_sdk.py`](../../../../../../experiments/inspect_sdk.py)

