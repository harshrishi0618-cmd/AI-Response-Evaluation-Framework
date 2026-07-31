from __future__ import annotations

from dataclasses import dataclass, field

from ai_response_eval.models.result import EvaluationResult


@dataclass(slots=True)
class EvaluationReport:
    """
    Aggregated report containing the results of all evaluators.
    """

    results: list[EvaluationResult] = field(default_factory=list)

    @property
    def overall_score(self) -> float:
        """Average percentage score across all metrics."""
        if not self.results:
            return 0.0

        return sum(result.percentage for result in self.results) / len(self.results)

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
    def passed(self) -> bool:
        return self.failed_metrics == 0

    def add_result(self, result: EvaluationResult) -> None:
        """Add a new evaluation result."""
        self.results.append(result)
