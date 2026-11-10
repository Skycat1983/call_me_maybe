# Learning Plan and Questions

> **Archived draft:** This combined document has been superseded by the
> [learning and progress log](../learning/index.md), numbered waypoint files,
> thematic reference pages, and the separate open-question register. It is
> retained to preserve the original annotations and answers.

The next step should be understanding the supplied materials—not implementing the decoder yet.

The project’s central idea is the separation of three responsibilities:

1. The LLM makes the semantic choice: “Which function and arguments best match this request?”

> **Question:** Where is the LLM, and does it get installed?
>
> **Answer:** The LLM is `Qwen/Qwen3-0.6B`, identified by the default
> `model_name` in `Small_LLM_Model.__init__`. `uv sync` installs the Python
> code needed to run it—PyTorch, Transformers, and Hugging Face Hub—but not
> the model weights themselves. The first construction of
> `Small_LLM_Model()` calls `from_pretrained(...)`, which downloads and caches
> the tokenizer and model weights. Because this profile has limited space, we
> should set `HF_HOME` to a location on the larger `/tmp` filesystem before
> that first load.

2. Constrained decoding controls generation: “Which next tokens are structurally allowed?”

> **Question:** What does “structurally allowed” mean?
>
> **Answer:** After the model scores every possible next token, our decoder
> rejects tokens that would make the required JSON impossible. For example,
> after `{"name":` a valid function-name string may be allowed, while `]` is
> not. Rejection is performed by replacing an invalid token's logit with
> negative infinity. The model still ranks the remaining valid choices.

3. Pydantic and JSON validation confirm the final result: “Does the completed value satisfy the contract?”

Keeping those responsibilities separate will make the eventual implementation much easier to reason about.

## Recommended learning sequence

### 1. Inspect the supplied data

Read:

- `data/input/function_calling_tests.json`
- `data/input/functions_definition.json`

The goal is to understand:

- How prompts are represented.

> **Answer:** Yes. The file's top level is a JSON array. Each element is an
> object with a `prompt` key whose value is a string.

- How functions and parameters are described.

> **Answer:** Yes, with one refinement: parameter names are not necessarily
> single letters. Examples include `a`, `name`, `source_string`, and `regex`.
> Each function object has `name`, `description`, `parameters`, and `returns`.
> `parameters` maps each parameter name to a schema containing its type.

- Which JSON types currently appear.

> **Answer:** There are two levels of type here. The files themselves use JSON
> arrays, objects, and strings. Inside the function schemas, the current
> declared parameter and return types are only `number` and `string`.
> Evaluation may provide other JSON-compatible types, such as `boolean`, so
> the eventual design should not assume only the examples will occur.

- How a prompt maps conceptually to a function call.

> **Answer:** It must not be keyword searching. The model receives the user
> prompt together with the available function names, descriptions, and
> schemas. Its learned language understanding should give a suitable function
> name a higher score. Words such as “sum” are useful evidence to the model,
> but our code may not implement rules such as `if "sum" in prompt`.
> Constrained decoding limits the output to available function names without
> deciding which name is semantically best.

- Which assumptions might break when evaluation replaces these files.

Deliverable: a short data-format reference and a list of unanswered questions. No production code yet.

### 2. Understand the supplied SDK

Walk through `llm_sdk/llm_sdk/__init__.py` method by method.

> **Question:** Why do some installations appear to be missing?
>
> **Answer:** Imports are resolved from the selected Python environment.
> `torch`, `transformers`, and `huggingface_hub` are dependencies of the local
> `llm-sdk` package. Our import-only experiment showed that the present
> `.venv` has PyTorch and Hugging Face Hub but is missing `transformers`, so
> the environment has not been fully synced with the current lockfile. This
> is separate from downloading the Qwen model files. See
> `docs/reference/imports.md`.

We should establish:

- How the model is loaded.

> **Answer:** Correct. This file defines the class but does not construct an
> instance. Future application code must import `Small_LLM_Model` and call
> `Small_LLM_Model()`. Its constructor selects a device and numeric precision,
> then `AutoTokenizer.from_pretrained(...)` and
> `AutoModelForCausalLM.from_pretrained(...)` load or download the tokenizer
> and model.

- What `encode()` returns.

> **Answer:** It converts text into token IDs and wraps them in a
> `torch.Tensor`. If a text becomes the IDs `[42, 105, 9]`, the method returns
> something shaped like `[[42, 105, 9]]`. Its shape is `[1, token_count]`:
> one batch containing one sequence. The values use integer dtype
> `torch.long`, and the tensor is placed on the selected CPU, CUDA, or MPS
> device.

- What `decode()` accepts.

> **Answer:** Its annotation accepts either a PyTorch tensor or a plain
> `list[int]` of token IDs. A tensor is converted to a Python list before the
> tokenizer reconstructs text. There is a possible interface mismatch to
> investigate: `encode()` returns a two-dimensional tensor, while tokenizer
> `decode()` normally expects a one-dimensional sequence. We should test
> whether `decode(encode(text))` needs `encoded[0]`.

- What logits represent.

> **Answer:** A logit is the model's raw, unnormalized score for one possible
> next token. Larger means the model considers that token more plausible in
> the current context. Logits are not probabilities, but applying softmax
> would convert them into probabilities. For constrained decoding, comparing
> scores is enough; invalid entries can be masked with negative infinity.

- What shape `get_logits_from_input_ids()` returns.

> **Answer:** The model initially returns a tensor shaped
> `[batch_size, sequence_length, vocabulary_size]`. The SDK selects
> `out.logits[0, -1]`: the first batch item and last input position. It then
> returns a one-dimensional `list[float]` of length `vocabulary_size`. Index
> `i` is the score for token ID `i`.

- What the vocabulary file contains.

> **Answer:** It is not stored in this repository. The tokenizer files belong
> to the model repository on Hugging Face. Calling
> `get_path_to_vocab_file()`, `get_path_to_merges_file()`, or
> `get_path_to_tokenizer_file()` downloads the requested file into the Hugging
> Face cache and returns its local path. The vocabulary maps token text to
> token IDs; `tokenizer.json` contains a more complete serialized tokenizer.

- Which SDK methods are public and permitted.

> **Answer:** The permitted public surface is the constructor plus `encode`,
> `decode`, `get_logits_from_input_ids`, `get_path_to_vocab_file`,
> `get_path_to_merges_file`, and `get_path_to_tokenizer_file`. Names beginning
> with `_`, such as `_model` and `_tokenizer`, are private and the subject
> explicitly forbids accessing them.

- What state the SDK manages internally.

> **Answer:** An instance stores the model identifier, selected computation
> device, numeric dtype, tokenizer, and loaded model in `_model_name`,
> `_device`, `_dtype`, `_tokenizer`, and `_model`. The underscore marks these
> as private implementation details. The constructor also puts the model in
> evaluation mode and disables gradients because this project performs
> inference, not training.

The important learning point is that the SDK does not generate the complete answer for us. It gives us the scores for possible next tokens; our code must decide which tokens are permitted.

Deliverable: `docs/reference/llm-sdk.md`.

### 3. Trace one generation step manually

Before writing a decoder, use a simple prompt and examine:

```text
text → token IDs → model logits → highest-scoring tokens
```

Questions to answer:

- What is a token?
- How does it differ from a character or word?
- Why might one token contain several characters?
- What does a logit mean?
- How do we prevent the model from selecting an invalid token?
- How does the selected token become part of the next model input?

Answers:

- A **token** is one vocabulary item represented by an integer ID.
- It is not necessarily a character or word. A tokenizer may represent a
  whole common word, punctuation, whitespace plus text, or a word fragment as
  one token.
- Multi-character tokens make common text more efficient and keep the
  vocabulary finite while still allowing uncommon words to be assembled from
  smaller pieces.
- A **logit** is the raw score for choosing one vocabulary token next.
- We prevent invalid selection by masking each invalid token's logit with
  negative infinity before selecting from the remaining candidates.
- We append the selected token ID to the current ID sequence. That longer
  sequence becomes the input to the next call, so generation is
  autoregressive: each new token is predicted from everything before it.

This should be a small learning experiment, not application code.

### 4. Understand partial validity

The decoder cannot simply ask whether the current output is valid JSON. During generation, strings such as these are incomplete but potentially valid:

```text
{
{"name
{"name":
{"name": "fn_
```

We need to distinguish:

- Valid and complete.
- Valid but incomplete.
- Impossible to complete validly.

This is the conceptual foundation for constrained decoding.

A useful exercise is designing a tiny state machine for one fixed structure:

```json
{"name":"fn_greet","parameters":{"name":"john"}}
```

Do this on paper or in documentation before generalizing it.

### 5. Design the application boundaries

Once the data and SDK are understood, define components such as:

```text
CLI
 └── input loader
      └── Pydantic models
           └── prompt construction
                └── constrained decoder
                     └── final validation
                          └── output writer
```

For each component, decide:

- What it receives.
- What it returns.
- Which errors it owns.
- What can be tested without loading the LLM.

Deliverable: `docs/design/architecture.md`.

### 6. Implement the simpler foundation

Only then begin application code:

1. Create `src/__init__.py` and `src/__main__.py`.
2. Parse command-line arguments.
3. Define Pydantic models.
4. Load and validate input JSON.
5. Write and validate output JSON.
6. Add tests for malformed and missing input.

At this stage, the function-calling result can remain unimplemented. The aim is to build a reliable shell around the difficult algorithm.

### 7. Build constrained decoding incrementally

A sensible order is:

1. Fixed literal text.
2. Function names from a finite list.
3. Object punctuation.
4. Parameter names.
5. Strings and escaping.
6. Numbers.
7. Booleans and any additional supported types.
8. Full schema transitions.
9. Completion and stopping behavior.

Each stage should have focused tests before proceeding.

### 8. Integrate the LLM

Once candidate-token filtering works independently:

- Get logits from the SDK.
- Mask invalid token logits.
- Select the best remaining token.
- Append it.
- Repeat.
- Confirm that the LLM determines semantic choices while the decoder enforces validity.

### 9. Evaluate and document

Finally:

- Measure function-selection accuracy.
- Confirm 100% JSON/schema validity.
- Measure runtime.
- Exercise alternate function definitions.
- Complete the required README.
- Work through the evaluation checklist.

## Immediate next activity

The best next session is a guided inspection of the two input files and `llm_sdk/llm_sdk/__init__.py`. We should explain each structure and method, record what we learn, and identify questions before creating any `src` implementation.
