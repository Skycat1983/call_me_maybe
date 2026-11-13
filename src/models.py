"""Validated data models for project inputs and outputs."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ParameterType = Literal["string", "number", "boolean"]


class PromptInput(BaseModel):
    """Represent one natural-language function-calling request."""

    model_config = ConfigDict(extra="forbid", strict=True)

    prompt: str = Field(min_length=1)


class ValueDefinition(BaseModel):
    """Describe the JSON type required for one function value."""

    model_config = ConfigDict(extra="forbid", strict=True)

    type: ParameterType


class FunctionDefinition(BaseModel):
    """Describe one function available to the language model."""

    model_config = ConfigDict(extra="forbid", strict=True)

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: dict[str, ValueDefinition]
    returns: ValueDefinition
