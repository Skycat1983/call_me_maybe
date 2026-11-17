"""Load untrusted JSON files into validated application models."""

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from src.models import FunctionDefinition, PromptInput


ModelT = TypeVar("ModelT", bound=BaseModel)


class InputLoadError(ValueError):
    """Report a clear, expected failure at the JSON input boundary."""


def _load_model_list(
    path: str | Path,
    model_type: type[ModelT],
    item_label: str,
) -> list[ModelT]:
    """Load a non-empty JSON array and validate each item as ``model_type``."""

    input_path = Path(path)

    try:
        with input_path.open(encoding="utf-8") as input_file:
            raw_data: object = json.load(input_file)
    except json.JSONDecodeError as error:
        raise InputLoadError(
            f"Invalid JSON in '{input_path}' at line {error.lineno}, "
            f"column {error.colno}: {error.msg}"
        ) from error
    except (OSError, UnicodeError) as error:
        raise InputLoadError(
            f"Could not read '{input_path}': {error}"
        ) from error

    if not isinstance(raw_data, list):
        raise InputLoadError(
            f"Expected a JSON array in '{input_path}', "
            f"got {type(raw_data).__name__}."
        )

    if not raw_data:
        raise InputLoadError(
            f"Expected at least one {item_label} in '{input_path}'."
        )

    validated_items: list[ModelT] = []

    for index, raw_item in enumerate(raw_data):
        try:
            validated_items.append(model_type.model_validate(raw_item))
        except ValidationError as error:
            raise InputLoadError(
                f"Invalid {item_label} at index {index} in '{input_path}': "
                f"{error}"
            ) from error

    return validated_items


def load_prompts(path: str | Path) -> list[PromptInput]:
    """Load and validate a non-empty array of prompt inputs."""

    return _load_model_list(path, PromptInput, "prompt")


def load_function_definitions(path: str | Path) -> list[FunctionDefinition]:
    """Load and validate a non-empty array of function definitions."""

    return _load_model_list(path, FunctionDefinition, "function definition")
