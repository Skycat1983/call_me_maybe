# Talking Points 014: CLI Input Shell

Companion waypoint:
[014 — CLI input shell](../../waypoints/014-2026-11-17-cli-input-shell.md)

## Files to have open

- [`src/cli.py`](../../../../src/cli.py) — the defaults, `CliPaths`, parser, typed conversion, and expected-error boundary.
- [`src/__main__.py`](../../../../src/__main__.py) — the module entry point that converts `main()`'s return value into a process exit code.
- [`tests/test_cli.py`](../../../../tests/test_cli.py) — the examples specifying defaults, overrides, streams, exit codes, and exception scope.
- [`src/loaders.py`](../../../../src/loaders.py) — the `InputLoadError` boundary caught by the CLI.
- [`Makefile`](../../../../Makefile) — the `run`, `debug`, and repaired `test` commands that enter the program.
- [Input/output contract](../../../requirements/input-output-contract.md) — the canonical flags and default paths.
- [CLI theme](../themes/command-line-interface/index.md) — the living topic guide for command-line concepts and project application.

## Agent preparation

Open the files above. Let the learner trace argument text into typed paths and
predict each exit code before explaining. Keep parsing, input validation, and
future generation as separate boundaries. Do not begin output or LLM
implementation unless the learner explicitly changes the session's purpose.

## Short recap

`python -m src` now parses the three required path options, validates both
input files, and reports expected input errors cleanly. Eight CLI tests cover
defaults, overrides, help, syntax errors, loader failures, and unexpected
exceptions. Successful validation intentionally writes no output yet.

## Conversation order

1. Follow `python -m src` into `src/__main__.py`.
2. Explain `main()`'s return value and `SystemExit`.
3. Build the `ArgumentParser` and inspect each option.
4. Compare omitted arguments with explicit overrides.
5. Convert the dynamic `Namespace` into frozen `CliPaths`.
6. Follow both loaders on the success path.
7. Trace `InputLoadError` to `stderr` and exit code `1`.
8. Compare help code `0`, runtime-input code `1`, and syntax code `2`.
9. Inspect how tests control arguments and capture streams.
10. State why output writing remains absent.

## Complete flow

```text
shell
  -> Python finds src/__main__.py
  -> __main__ calls cli.main()
  -> parse_args() calls build_parser()
  -> argparse produces Namespace
  -> CliPaths validates three Path values
  -> load_prompts(paths.input)
  -> load_function_definitions(paths.functions_definition)
  -> success: return 0
  -> expected input failure: stderr + return 1
  -> SystemExit exposes the code to the shell
```

## Values to trace

| Name | Type | Role |
|---|---|---|
| `arguments` | `Sequence[str] | None` | Test-provided values or real process arguments |
| `parser` | `ArgumentParser` | Flag definitions, defaults, help, and syntax handling |
| `namespace` | `Namespace` | Dynamic intermediate result owned by argparse |
| `paths` | `CliPaths` | Strict typed configuration used by project code |
| `error` | `InputLoadError` | Expected file or validation failure |
| `exit_code` | `int` | Result interpreted by the shell |

## Discussion prompts

- What file does Python seek when it runs `python -m src`?
- Why does the module guard raise `SystemExit(main())`?
- Who owns invalid flag syntax: our code or argparse?
- Why does `type=Path` matter before `CliPaths` validation?
- What problem do the three `cast(Path, ...)` calls solve for Mypy?
- Why use a Pydantic model instead of passing `Namespace` onward?
- Why is the output path parsed even though it is not used yet?
- What belongs on `stdout`, and what belongs on `stderr`?
- Which exception is expected, and why are others allowed to escape?
- Why does the success test assert that the output path does not exist?

## Understanding checks

Ask the learner to predict:

- every field in `parse_args([])`;
- the type of an explicitly supplied path;
- the exit code for `--help`;
- the exit code for `--input` without a value;
- the exit code for a missing JSON file;
- whether a missing file produces a traceback;
- whether a `RuntimeError` is caught;
- whether a successful validation run writes `function_calls.json`.

## Likely misconceptions

- `python -m src` executes `src/__main__.py`, not `src/__init__.py`.
- Argparse's `Namespace` is an intermediate object, not the project API.
- `Path` represents a path; parsing it does not open the file.
- `stderr` is not an exception or an exit code; it is an output stream.
- Catching expected input errors does not justify catching every exception.
- Exit code `0` currently means input validation succeeded, not that function
  calls were generated.

## Related thematic learning

- [Command-line interface](../themes/command-line-interface/index.md)
- [Input validation and data models](../themes/input-validation/index.md)
- [Talking points 013 — JSON loading boundary](013-json-loading-boundary.md)
- [Python project tooling](../themes/python-tooling/index.md)

## Successful session outcome

The learner can trace the real module entry through parsing and loading,
explain typed CLI configuration, predict streams and exit codes, and identify
the precise boundary between completed input validation and future output
generation.
