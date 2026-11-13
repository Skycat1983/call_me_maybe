"""Tests for the project's Pydantic data models."""

import json
from pathlib import Path
from typing import cast

import pytest
from pydantic import ValidationError

from src.models import FunctionDefinition, PromptInput, ValueDefinition


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIRECTORY = PROJECT_ROOT / "data" / "input"


def load_object_list(filename: str) -> list[dict[str, object]]:
    """Load a demonstration JSON array for validation tests."""

    path = INPUT_DIRECTORY / filename
    loaded = json.loads(path.read_text(encoding="utf-8"))
    return cast(list[dict[str, object]], loaded)


def test_supplied_prompts_validate() -> None:
    """Accept every prompt object supplied with the project."""

    raw_prompts = load_object_list("function_calling_tests.json")

    prompts = [PromptInput.model_validate(item) for item in raw_prompts]

    assert len(prompts) == 11
    assert prompts[0].prompt == "What is the sum of 2 and 3?"


def test_supplied_function_definitions_validate() -> None:
    """Accept every function definition supplied with the project."""

    raw_definitions = load_object_list("functions_definition.json")

    definitions = [
        FunctionDefinition.model_validate(item) for item in raw_definitions
    ]

    assert len(definitions) == 5
    assert definitions[0].parameters["a"].type == "number"


def test_prompt_requires_prompt_field() -> None:
    """Reject a prompt object with no prompt field."""

    with pytest.raises(ValidationError):
        PromptInput.model_validate({})


def test_prompt_rejects_empty_text() -> None:
    """Reject an empty natural-language prompt."""

    with pytest.raises(ValidationError):
        PromptInput.model_validate({"prompt": ""})


def test_prompt_rejects_non_string_text() -> None:
    """Reject a prompt value instead of coercing it into text."""

    with pytest.raises(ValidationError):
        PromptInput.model_validate({"prompt": 42})


def test_prompt_rejects_extra_fields() -> None:
    """Reject fields outside the documented prompt schema."""

    with pytest.raises(ValidationError):
        PromptInput.model_validate({"prompt": "Greet Ada", "extra": True})


def test_value_definition_rejects_unknown_type() -> None:
    """Reject parameter types outside the initially supported set."""

    with pytest.raises(ValidationError):
        ValueDefinition.model_validate({"type": "array"})


@pytest.mark.parametrize("value_type", ["string", "number", "boolean"])
def test_supported_value_types_validate(value_type: str) -> None:
    """Accept each value type required by the initial project scope."""

    definition = ValueDefinition.model_validate({"type": value_type})

    assert definition.type == value_type


def test_function_definition_rejects_missing_fields() -> None:
    """Reject a function definition without its required description."""

    invalid_definition = {
        "name": "fn_greet",
        "parameters": {"name": {"type": "string"}},
        "returns": {"type": "string"},
    }

    with pytest.raises(ValidationError):
        FunctionDefinition.model_validate(invalid_definition)


def test_function_definition_rejects_extra_fields() -> None:
    """Reject fields outside the documented function schema."""

    invalid_definition = {
        "name": "fn_greet",
        "description": "Greet a person.",
        "parameters": {"name": {"type": "string"}},
        "returns": {"type": "string"},
        "extra": "not allowed",
    }

    with pytest.raises(ValidationError):
        FunctionDefinition.model_validate(invalid_definition)


def test_function_definition_rejects_non_mapping_parameters() -> None:
    """Reject a parameter collection with the wrong runtime type."""

    invalid_definition = {
        "name": "fn_greet",
        "description": "Greet a person.",
        "parameters": ["name"],
        "returns": {"type": "string"},
    }

    with pytest.raises(ValidationError):
        FunctionDefinition.model_validate(invalid_definition)
