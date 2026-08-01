from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvaluationRequest:
    """
    Represents all information required to evaluate an AI-generated response.
    """

    prompt: str
    response: str
    reference: str | None = None
    model_name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
