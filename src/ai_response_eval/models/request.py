from dataclasses import dataclass


@dataclass(slots=True)
class EvaluationRequest:
    """
    Input for an evaluation.
    """

    prompt: str
    response: str
    reference: str | None = None
    model_name: str | None = None
