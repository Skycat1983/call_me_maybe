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
