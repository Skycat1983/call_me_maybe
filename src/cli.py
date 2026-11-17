"""Parse command-line paths and validate the application's input files."""

import sys
from argparse import ArgumentParser
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from pydantic import BaseModel, ConfigDict

from src.loaders import (
    InputLoadError,
    load_function_definitions,
    load_prompts,
)


DEFAULT_FUNCTION_DEFINITIONS_PATH = Path(
    "data/input/functions_definition.json"
)
DEFAULT_INPUT_PATH = Path("data/input/function_calling_tests.json")
DEFAULT_OUTPUT_PATH = Path("data/output/function_calls.json")


class CliPaths(BaseModel):
    """Store the input and output paths selected through the CLI."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    functions_definition: Path
    input: Path
    output: Path


def build_parser() -> ArgumentParser:
    """Create the command-line parser for project file paths."""

    parser = ArgumentParser(
        prog="python -m src",
        description="Generate constrained function calls from prompt JSON.",
    )
    parser.add_argument(
        "--functions_definition",
        type=Path,
        default=DEFAULT_FUNCTION_DEFINITIONS_PATH,
        metavar="PATH",
        help="function-definition JSON path",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        metavar="PATH",
        help="prompt-input JSON path",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        metavar="PATH",
        help="generated function-call JSON path",
    )
    return parser


def parse_args(arguments: Sequence[str] | None = None) -> CliPaths:
    """Parse command-line text into a typed path model."""

    namespace = build_parser().parse_args(arguments)
    return CliPaths(
        functions_definition=cast(Path, namespace.functions_definition),
        input=cast(Path, namespace.input),
        output=cast(Path, namespace.output),
    )


def main(arguments: Sequence[str] | None = None) -> int:
    """Validate CLI-selected inputs and return a process exit code."""

    paths = parse_args(arguments)

    try:
        load_prompts(paths.input)
        load_function_definitions(paths.functions_definition)
    except InputLoadError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    return 0
