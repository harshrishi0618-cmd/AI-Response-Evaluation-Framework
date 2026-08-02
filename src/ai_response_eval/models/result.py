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

    # Relative importance of this metric.
    # Default keeps backward compatibility.
    weight: float = 1.0

    @property
    def percentage(self) -> float:
        """
        Converts a 0–10 score into a percentage.
        """
        score = max(0.0, min(self.score, 10.0))
        return round(score * 10.0, 2)
