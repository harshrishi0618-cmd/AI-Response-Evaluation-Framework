from __future__ import annotations

from dataclasses import dataclass, field

from ai_response_eval.models.result import EvaluationResult


@dataclass
class EvaluationReport:
    """
    Represents the complete evaluation report.
    """

    results: list[EvaluationResult] = field(default_factory=list)

    def add_result(self, result: EvaluationResult) -> None:
        """Add an evaluation result to the report."""
        self.results.append(result)

    @property
    def total_metrics(self) -> int:
        return len(self.results)

    @property
    def passed_metrics(self) -> int:
        return sum(result.passed for result in self.results)

    @property
    def failed_metrics(self) -> int:
        return self.total_metrics - self.passed_metrics

    @property
    def overall_score(self) -> float:
        """
        Average score of all evaluators.
        """
        if not self.results:
            return 0.0

        return round(
            sum(result.score for result in self.results) / self.total_metrics,
            2,
        )

    @property
    def pass_rate(self) -> float:
        """
        Percentage of evaluators that passed.
        """
        if not self.results:
            return 0.0

        return round(
            self.passed_metrics / self.total_metrics,
            2,
        )

    @property
    def passed(self) -> bool:
        """
        Overall evaluation status.
        """
        if not self.results:
            return True

        return self.pass_rate >= 0.70

    def summary(self) -> str:
        return (
            f"{self.passed_metrics}/{self.total_metrics} metrics passed "
            f"(overall score: {self.overall_score:.2f})"
        )
