from dataclasses import dataclass


@dataclass
class ScoreBuilder:
    """
    Utility class for calculating evaluation scores.
    """

    initial_score: float = 10.0
    maximum_score: float = 10.0
    minimum_score: float = 0.0

    def __post_init__(self):
        self.score = self.initial_score

    def penalize(self, condition: bool, points: float) -> None:
        if condition:
            self.score -= points

    def reward(self, condition: bool, points: float) -> None:
        if condition:
            self.score += points

    def clamp(self) -> float:
        self.score = max(self.minimum_score, self.score)
        self.score = min(self.maximum_score, self.score)
        return round(self.score, 2)
