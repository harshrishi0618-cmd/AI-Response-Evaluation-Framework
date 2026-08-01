from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """
    Represents the result produced by a single evaluator.
    """

    metric_name: str
    score: float
    feedback: str
    passed: bool
    weight: float = 1.0

    @property
    def percentage(self) -> float:
        """
        Returns the score as a percentage.
        """
        return round(self.score * 100, 2)
