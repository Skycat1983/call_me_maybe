# Runtime Flow: Model Construction

- Kind: Thematic talking point
- Theme: LLM SDK and `inspect_sdk`
- Depth: Detailed execution stage 6
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: [Command and entry](command-and-entry.md)

## Stage 6: Construct `Small_LLM_Model`

The key boundary crossing is:

```python
model = Small_LLM_Model(device=requested_device)
```

The script calls the supplied class. Python allocates an instance and invokes
its `__init__()` method. `model` receives the instance only after construction
finishes successfully.

### Constructor arguments

The signature is conceptually:

```python
Small_LLM_Model(
    model_name="Qwen/Qwen3-0.6B",
    *,
    device=None,
    dtype=None,
    trust_remote_code=True,
)
```

| Parameter | CPU run value | Meaning |
|---|---|---|
| `self` | new instance | Object currently being initialized |
| `model_name` | `"Qwen/Qwen3-0.6B"` | Hugging Face repository identifier |
| `device` | `"cpu"` | Computation backend |
| `dtype` | `None`, then selected | Numerical precision |
| `trust_remote_code` | `True` | Permit model repository implementation code when needed |

The bare `*` makes later parameters keyword-only. A caller must write
`device="cpu"`; a positional second argument is not accepted.

### `self`

`self` is the new instance. Assignments such as:

```python
self._device = device
```

store state on that object so later method calls can reuse it. Local variables
disappear when `__init__()` returns; instance attributes remain while `model`
exists.

### Step 6.1: Store the model identifier

```python
self._model_name = model_name
```

State after assignment:

```text
self._model_name
type: str
value: "Qwen/Qwen3-0.6B"
later consumer: tokenizer-file getter methods
```

The leading underscore marks internal SDK state. The project is allowed to
use public methods, not reach into `_model_name`, `_tokenizer`, or `_model`.
This guide explains internals for learning; it does not grant application code
permission to use private members.

### Step 6.2: Select the device

If `device is None`, the class checks:

```text
MPS available?  -> use mps
else CUDA?      -> use cuda
else            -> use cpu
```

The explicit CPU run skips those availability checks because `device` already
holds `"cpu"`.

```python
self._device = device
```

After assignment, `_device` tells later tensor creation and model movement
where computation should occur.

### Step 6.3: Select the dtype

`dtype` means data type: how model numbers are represented.

If no dtype was supplied:

```text
cuda or mps -> torch.float16
cpu         -> torch.float32
```

For the successful run:

```text
self._dtype
type: torch.dtype
value: torch.float32
```

Float16 uses less memory but CPU compatibility is generally safer with
float32 in this wrapper.

### Step 6.4: Load the tokenizer

```python
self._tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=trust_remote_code,
)
```

The tokenizer is not the neural network. It is the text/token-ID translator.
Transformers uses the model identifier to choose the appropriate tokenizer
implementation and loads its configuration/files from the Hugging Face cache,
downloading them when absent.

State afterward:

```text
self._tokenizer
declared type: PreTrainedTokenizer
runtime role: encode text, decode IDs, expose tokenizer file names
lifetime: retained by the SDK instance
```

If no padding token exists, the wrapper assigns the end-of-sequence token as
the padding token. This gives batch-oriented helpers a valid padding ID.

### Step 6.5: Load the causal language model

```python
self._model = AutoModelForCausalLM.from_pretrained(...)
```

“Causal language model” means a model trained to score the next token from the
tokens that came before it.

Important arguments:

| Argument | CPU run meaning |
|---|---|
| `model_name` | Load Qwen3-0.6B metadata and weights |
| `torch_dtype=self._dtype` | Use float32 parameters |
| `device_map=None` | Do not use automatic CUDA mapping |
| `trust_remote_code=True` | Permit repository-specific implementation when needed |

For an explicit CUDA device, the wrapper passes `device_map="auto"`. That
branch produced the earlier `accelerate` error during the default experiment.

### Step 6.6: Prepare the model for inference

```python
self._model.to(self._device)
self._model.eval()
```

`.to("cpu")` places model parameters on CPU. `.eval()` switches modules such
as dropout into evaluation behavior. It does not perform an inference call.

Then every model parameter has:

```python
p.requires_grad = False
```

Each `p` is one `torch.nn.Parameter` encountered by the loop. Disabling
gradients avoids training-related work because this project performs
inference only.

### Step 6.7: Return to the probe

`__init__()` returns `None` implicitly, but the class call expression returns
the newly initialized instance. The script binds it to `model`.

```text
model
type: Small_LLM_Model
holds internally: model identifier, device, dtype, tokenizer, neural model
```

The timing variables are floating-point counter readings:

```text
construction_started   counter value before class call
construction_seconds   counter difference after successful construction
observed CPU duration  18.419 seconds in the recorded run
```

This is one observation, not a guaranteed benchmark.

## Related learning

- [Runtime-flow map](index.md)
- [Previous: command and entry](command-and-entry.md)
- [Next: encoding and decoding](encoding-and-decoding.md)
- [`Small_LLM_Model` source](../../../../../../llm_sdk/llm_sdk/__init__.py)
- [Known issues](../../../../../project/issues.md)

