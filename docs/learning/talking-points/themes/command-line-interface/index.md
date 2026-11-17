# Theme: Command-Line Interface

- Kind: Thematic talking-point index
- Status: Living
- Last reviewed: 2026-11-17
- Prerequisites: Basic functions, exceptions, and file paths

## Files to have open

- [`src/cli.py`](../../../../../src/cli.py) — the parser, default paths, typed `CliPaths`, and expected-error handling.
- [`src/__main__.py`](../../../../../src/__main__.py) — the module execution boundary and process exit.
- [`tests/test_cli.py`](../../../../../tests/test_cli.py) — executable examples of arguments, help, streams, and exit codes.
- [`src/loaders.py`](../../../../../src/loaders.py) — the application error type and input functions used by `main()`.
- [`Makefile`](../../../../../Makefile) — human-facing commands that invoke the module and test suite.
- [Input/output contract](../../../../requirements/input-output-contract.md) — the canonical CLI spelling, defaults, and expected file roles.

## Purpose

Use this theme to understand how shell arguments enter the Python application,
become typed path configuration, reach the loader boundary, and return useful
process outcomes. It will grow when output writing and the full application
pipeline are connected.

## Five-minute mental model

```text
command text
    -> argparse syntax and defaults
    -> dynamic Namespace
    -> strict CliPaths model
    -> application input loaders
    -> return code
    -> SystemExit
    -> shell observes success or failure
```

There are three different channels to keep separate:

| Channel | Current use |
|---|---|
| Standard output | Reserved for ordinary program information; currently empty |
| Standard error | One-line expected input diagnostics |
| Exit code | Machine-readable success or failure status |

## Module execution

Python treats a package as executable when it contains `__main__.py`:

```bash
python -m src
```

Python imports and executes `src/__main__.py`. That file calls `main()` and
raises `SystemExit` with the returned integer. The shell does not see a Python
return value directly; it sees the resulting process exit status.

`src/__init__.py` still defines the package. It is not the module entry point.

## Parsing responsibilities

`build_parser()` owns command syntax:

- `--functions_definition PATH`;
- `--input PATH`;
- `--output PATH`;
- help text;
- documented relative defaults;
- invalid flag and missing-value behavior.

All three flags are optional because each has a default. `type=Path` converts
argument text into a `Path` object; it does not open the file or prove that it
exists.

## Typed configuration

Argparse returns a `Namespace` whose attributes are created dynamically.
`parse_args()` immediately converts those attributes into `CliPaths`, a strict
and frozen Pydantic model.

The conversion gives project code:

- declared field names and `Path` types;
- runtime validation;
- Mypy-visible structure;
- rejection of unexpected fields;
- protection against later reassignment.

The `cast(Path, ...)` calls communicate argparse's configured runtime result to
the static type checker. They do not convert or validate values at runtime;
`type=Path` and Pydantic perform those runtime roles.

## Error and exit-code policy

| Situation | Owner | Stream | Exit code |
|---|---|---|---|
| Valid input paths and files | `main()` | none | `0` |
| `--help` | argparse | stdout | `0` |
| Unknown flag or missing flag value | argparse | stderr | `2` |
| Expected file or validation failure | `main()` | stderr | `1` |
| Unexpected programming exception | Python | traceback | nonzero |

Only `InputLoadError` is translated into the expected one-line application
diagnostic. This narrow catch makes ordinary user input safe without hiding
defects that developers need to see and repair.

## Why output is not written yet

The CLI already accepts and stores the required output path because that path
is part of the stable interface. It does not create the file because there are
no generated `FunctionCall` records yet. This preserves a useful invariant:
an output file should mean that real results were serialized, not merely that
input validation passed.

## What the tests prove

[`tests/test_cli.py`](../../../../../tests/test_cli.py) proves:

- defaults and explicit overrides produce the expected `Path` values;
- help and syntax errors retain argparse behavior;
- valid input files pass through the CLI boundary;
- successful validation does not create an output file;
- expected loader errors use `stderr`, code `1`, and no traceback;
- an unexpected `RuntimeError` is not hidden.

The tests do not yet prove:

- output records can be serialized;
- parent output directories are created or validated;
- write failures are presented cleanly;
- the LLM or constrained decoder runs;
- a completed invocation produces required function calls.

## Voice-session routes

- **Overview:** follow the five-minute mental model and channel table.
- **Execution:** trace `python -m src` through `__main__.py` and `main()`.
- **Parsing:** inspect parser definitions, defaults, `Namespace`, and
  `CliPaths`.
- **Errors:** predict owner, stream, and exit code for each failure.
- **Tests:** predict each outcome before reading the corresponding assertion.
- **Design boundary:** explain why output and model work are deliberately
  absent.

## Questions to revisit as the theme grows

- Should successful completed runs write anything to stdout?
- Should output parent directories be created automatically?
- How should an output-write error differ from `InputLoadError`?
- Does the final application need additional device or model flags?
- At what layer should end-to-end timing be measured?

## Related learning

- [Talking-points hub](../../index.md)
- [Thematic discussions](../index.md)
- [Waypoint 014 discussion](../../waypoints/014-cli-input-shell.md)
- [Waypoint 014 record](../../../waypoints/014-2026-11-17-cli-input-shell.md)
- [Input validation and data models](../input-validation/index.md)
- [Python project tooling](../python-tooling/index.md)
- [Implementation rules](../../../../requirements/implementation-rules.md)
- [Project status](../../../../project/status.md)
