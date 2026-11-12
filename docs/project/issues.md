# Known Issues

This register contains observed problems. Planned features belong in
`tasks.md`; unresolved design choices belong in `questions.md`.

## I-001: Project environment is not fully synchronized

- Status: Resolved
- Severity: Was blocking SDK experiments
- Observed: Waypoint 004
- Resolved: [Waypoint 005](../learning/waypoints/005-2026-11-10-environment-repair-and-cache-placement.md)

### Evidence

An import-only command failed:

```text
ModuleNotFoundError: No module named 'transformers'
```

The original `.venv` contained `torch`, `huggingface-hub`, and `llm-sdk`, but
did not contain `transformers`, even though it is a dependency of `llm-sdk`.

### Resolution

The Makefile now exports `UV_PROJECT_ENVIRONMENT`,
`UV_CACHE_DIR`, and `HF_HOME` paths under `/tmp`. A complete `make install`
created the relocated environment and an import-only check succeeded with
`transformers 5.20.2`.

The incomplete local `.venv` was removed after verification.

## I-002: Supplied SDK does not currently pass Flake8

- Status: Open
- Severity: Non-blocking during interface study
- Observed: Waypoint 004

### Evidence

A targeted Flake8 run reports pre-existing long lines and extra blank lines in
`llm_sdk/llm_sdk/__init__.py`.

### Next action

Decide whether the copied SDK is in project lint scope. If it is, format it
without changing behavior and rerun the mandatory `flake8 .` command.

## I-003: Model construction requires accelerate

- Status: Open; explicit-CPU workaround confirmed
- Severity: Blocks observed automatic/default loading, not CPU experiments
- Observed: [Waypoint 006](../learning/waypoints/006-2026-11-10-first-sdk-probe.md)
- Workaround: [Waypoint 007](../learning/waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md)

### Evidence

Default `Small_LLM_Model()` construction reached
`AutoModelForCausalLM.from_pretrained(...)` and failed in Transformers'
device-map check:

```text
ValueError: Using a device_map ... requires accelerate.
```

The root environment uses Transformers `5.20.2` and PyTorch `2.14.1`. The
supplied SDK lock records Transformers `5.0.0` and PyTorch `2.10.0`. Neither
dependency set includes `accelerate`.

### Updated impact

Default construction did not create a model. Explicit
`Small_LLM_Model(device="cpu")` successfully loaded the model and enabled
encoding, decoding, tokenizer-file, and logits observations.

### Next action

Resolve `Q-007` before deciding whether production should force CPU, expose a
device option, pin supplied versions, or declare `accelerate`.

## I-004: Decode return type depends on tensor dimensionality

- Status: Open
- Severity: Non-blocking SDK interface mismatch
- Observed: [Waypoint 007](../learning/waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md)

### Evidence

The SDK annotation promises `str`, but the public method returned:

```text
decode(encoded)    -> list[str]
decode(encoded[0]) -> str
```

`encode()` returns a batched two-dimensional tensor. Passing the first row
gives the one-dimensional token sequence expected for a single decoded string.

### Next action

Use a one-dimensional sequence in project code. Later decide whether to repair
the copied SDK's annotation/behavior or document the required call shape.

## I-005: Editor workflow recreated a local project environment

- Status: Resolved
- Severity: Was blocking due to profile storage exhaustion
- Observed and resolved: [Waypoint 008](../learning/waypoints/008-2026-11-12-editor-navigation-and-environment-storage.md)

### Evidence

A newly created repository `.venv` used 1.1 GB and reduced the 4.7 GB home
filesystem to 60 MB free. Its `pyvenv.cfg` identified uv 0.12.5 as its creator.
The complete environment still existed under `/tmp`.

The timing followed VS Code interpreter configuration, but does not prove that
interpreter selection itself created the environment. An environment action or
uv command outside Make would not inherit Makefile-only path variables.

### Resolution

The incomplete duplicate was removed. `.venv` is now an ignored symbolic link
to `/tmp/call-me-maybe-venv`; project-level uv settings keep its cache under
`/tmp`; and VS Code workspace settings select the linked interpreter, expose
the local SDK source, and pass the storage variables to editor processes and
new integrated terminals.
