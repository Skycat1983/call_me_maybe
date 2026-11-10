# Known Issues

This register contains observed problems. Planned features belong in
`tasks.md`; unresolved design choices belong in `questions.md`.

## I-001: Project environment is not fully synchronized

- Status: Open
- Severity: Blocking SDK experiments
Observed: Waypoint 004

### Evidence

An import-only command failed:

```text
ModuleNotFoundError: No module named 'transformers'
```

The current `.venv` contains `torch`, `huggingface-hub`, and `llm-sdk`, but
does not contain `transformers`, even though it is a dependency of
`llm-sdk`.

### Next action

Run a complete `uv sync`, then repeat the import-only check before downloading
or constructing the Qwen model.

## I-002: Supplied SDK does not currently pass Flake8

- Status: Open
- Severity: Non-blocking during interface study
Observed: Waypoint 004

### Evidence

A targeted Flake8 run reports pre-existing long lines and extra blank lines in
`llm_sdk/llm_sdk/__init__.py`.

### Next action

Decide whether the copied SDK is in project lint scope. If it is, format it
without changing behavior and rerun the mandatory `flake8 .` command.
