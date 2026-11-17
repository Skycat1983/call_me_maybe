# Waypoint 014: CLI Input Shell

- Date: 2026-11-17
- Stage: Application command-line boundary
- Status: Complete

Voice discussion:
[Talking points 014](../talking-points/waypoints/014-cli-input-shell.md)

## Purpose

Make `python -m src` accept the three documented file-path options, apply the
required defaults, validate both input files, and present ordinary input
failures without an unexpected traceback.

## Boundary implemented

```text
shell argument text
    -> argparse Namespace
    -> CliPaths Pydantic model
    -> prompt and function-definition loaders
    -> exit code 0 or a concise expected error on stderr
```

The CLI accepts the output path but deliberately does not create the output
file yet. Output models, generation, and writing remain later boundaries.

## Code created

### `src/cli.py`

The module defines the documented default paths and four responsibilities:

- `CliPaths` stores three typed `Path` values in a strict, frozen Pydantic
  model;
- `build_parser()` defines the help text and optional path flags;
- `parse_args()` converts argparse's dynamic `Namespace` into `CliPaths`;
- `main()` validates both selected input files and returns a process exit code.

`main()` catches only `InputLoadError`. It writes expected input failures to
`stderr` and returns `1`. Argparse retains its conventional `0` for help and
`2` for invalid command syntax. Unexpected exceptions are not hidden behind a
broad catch.

### `src/__main__.py`

Python executes this module for `python -m src`. The module calls `main()` and
raises `SystemExit` with its returned code so shell callers can distinguish
success from failure.

### `tests/test_cli.py`

Eight focused tests prove:

- no arguments produce the documented default paths;
- all three paths can be overridden;
- parsed values become `Path` objects inside `CliPaths`;
- `--help` exits successfully;
- unknown arguments and missing flag values use argparse exit code `2`;
- valid inputs return `0` without writing a premature output file;
- expected loader failures use `stderr`, return `1`, and show no traceback;
- unexpected errors remain visible to developers.

## Questions and answers

### Why convert `Namespace` into `CliPaths`?

Argparse creates attributes dynamically. Converting immediately gives the rest
of the project a named, type-checked, runtime-validated object. `CliPaths` also
satisfies the project rule that project classes use Pydantic.

### Why is `CliPaths` frozen?

The selected paths are configuration for one run. Preventing later mutation
makes it easier to reason about which paths the application is using.

### Why accept `Sequence[str] | None`?

`None` tells argparse to read the real process arguments. Tests can instead
pass an explicit sequence without mutating global `sys.argv`.

### Why use different exit codes?

- `0` means the requested CLI action succeeded, including `--help`;
- `1` means valid command syntax reached an expected file or validation
  failure;
- `2` is argparse's conventional code for invalid command syntax.

### Why print expected errors to `stderr`?

Standard output is available for ordinary program results. Diagnostics belong
on the error stream, allowing shell users and evaluators to treat the streams
separately.

### Why catch only `InputLoadError`?

It is the expected application boundary established by the loaders. Catching
all exceptions would incorrectly turn programming defects into ordinary user
errors and make debugging harder.

### Why does a successful run not write output yet?

No function-call results exist before model selection and constrained
decoding. Creating an empty or fabricated output file would imply completed
work and could overwrite a path without meaningful data.

## Validation evidence

```text
python -m pytest tests/test_cli.py   -> 8 passed
make test                            -> 30 passed
flake8 src/cli.py src/__main__.py tests/test_cli.py
                                     -> no findings
mypy src/cli.py src/__main__.py tests/test_cli.py
                                     -> no issues in 3 source files
make run                             -> exit 0 with valid default inputs
python -m src --help                 -> three documented path options
```

## Decisions

- Default paths remain relative to the process working directory as documented
  by the subject.
- The CLI parses but does not yet use the output path.
- Expected input failures return `1` and write one diagnostic to `stderr`.
- Argparse owns help and command-syntax behavior.
- Unexpected exceptions remain uncaught.
- No LLM or output-writing code belongs in this shell.

## Documents created or updated

- [`src/cli.py`](../../../src/cli.py)
- [`src/__main__.py`](../../../src/__main__.py)
- [`tests/test_cli.py`](../../../tests/test_cli.py)
- [CLI theme](../talking-points/themes/command-line-interface/index.md)
- [Input-validation theme](../talking-points/themes/input-validation/index.md)
- [Project tasks](../../project/tasks.md)
- [Project status](../../project/status.md)

## Next step

Discuss the command-to-loader flow, then define and test the exact output
record model and JSON-writing boundary before beginning LLM integration.
