"""Tests for loading untrusted JSON into validated application models."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.loaders import (
    InputLoadError,
    load_function_definitions,
    load_prompts,
)
from src.models import FunctionDefinition, PromptInput


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIRECTORY = PROJECT_ROOT / "data" / "input"


def write_json(path: Path, value: object) -> Path:
    """Write one JSON test fixture and return its path."""

    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_load_supplied_prompts() -> None:
    """Return typed prompt models in their original order."""

    path = INPUT_DIRECTORY / "function_calling_tests.json"

    prompts = load_prompts(path)

    assert len(prompts) == 11
    assert all(isinstance(prompt, PromptInput) for prompt in prompts)
    assert prompts[0].prompt == "What is the sum of 2 and 3?"


def test_load_supplied_function_definitions() -> None:
    """Return typed function definitions with nested value models."""

    path = INPUT_DIRECTORY / "functions_definition.json"

    definitions = load_function_definitions(str(path))

    assert len(definitions) == 5
    assert all(
        isinstance(definition, FunctionDefinition)
        for definition in definitions
    )
    assert definitions[0].parameters["a"].type == "number"


def test_missing_file_reports_read_failure(tmp_path: Path) -> None:
    """Translate a missing file into an application input error."""

    missing_path = tmp_path / "missing.json"

    with pytest.raises(InputLoadError, match="Could not read") as caught:
        load_prompts(missing_path)

    assert isinstance(caught.value.__cause__, FileNotFoundError)


def test_invalid_json_reports_location(tmp_path: Path) -> None:
    """Report JSON syntax failure with its line and column."""

    path = tmp_path / "invalid.json"
    path.write_text('[{"prompt": "unfinished"}', encoding="utf-8")

    with pytest.raises(InputLoadError, match=r"line 1, column \d+") as caught:
        load_prompts(path)

    assert isinstance(caught.value.__cause__, json.JSONDecodeError)


def test_invalid_utf8_reports_read_failure(tmp_path: Path) -> None:
    """Translate text-decoding failure into an application input error."""

    path = tmp_path / "invalid-utf8.json"
    path.write_bytes(b"\xff")

    with pytest.raises(InputLoadError, match="Could not read") as caught:
        load_prompts(path)

    assert isinstance(caught.value.__cause__, UnicodeDecodeError)


def test_non_array_top_level_is_rejected(tmp_path: Path) -> None:
    """Require the JSON document itself to contain an array."""

    path = write_json(tmp_path / "object.json", {"prompt": "Hello"})

    with pytest.raises(
        InputLoadError,
        match=r"Expected a JSON array.*got dict",
    ):
        load_prompts(path)


def test_empty_array_is_rejected(tmp_path: Path) -> None:
    """Reject an input array that contains no work items."""

    path = write_json(tmp_path / "empty.json", [])

    with pytest.raises(InputLoadError, match="at least one prompt"):
        load_prompts(path)


def test_invalid_item_reports_array_index(tmp_path: Path) -> None:
    """Identify which array item failed Pydantic validation."""

    path = write_json(
        tmp_path / "prompts.json",
        [{"prompt": "Valid"}, {"prompt": 42}],
    )

    with pytest.raises(InputLoadError, match="prompt at index 1") as caught:
        load_prompts(path)

    assert isinstance(caught.value.__cause__, ValidationError)


def test_invalid_function_definition_uses_specific_label(
    tmp_path: Path,
) -> None:
    """Name the failed definition boundary in its error message."""

    path = write_json(
        tmp_path / "functions.json",
        [
            {
                "name": "fn_example",
                "description": "Example.",
                "parameters": {},
                "returns": {"type": "array"},
            }
        ],
    )

    with pytest.raises(
        InputLoadError,
        match="function definition at index 0",
    ) as caught:
        load_function_definitions(path)

    assert isinstance(caught.value.__cause__, ValidationError)
