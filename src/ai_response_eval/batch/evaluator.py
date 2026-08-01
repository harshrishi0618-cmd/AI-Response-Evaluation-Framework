from __future__ import annotations

from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.models.request import EvaluationRequest


class BatchEvaluator:
    """
    Evaluates multiple prompt-response pairs using a shared EvaluationEngine.
    """

    def __init__(self, engine: EvaluationEngine):
        self.engine = engine

    def evaluate(
        self,
        requests: list[EvaluationRequest],
    ) -> list[EvaluationReport]:
        """
        Evaluate every request and return a list of reports.
        """

        if not requests:
            raise ValueError("No evaluation requests provided.")

        reports: list[EvaluationReport] = []

        for request in requests:
            report = self.engine.evaluate(request)
            reports.append(report)

        return reports

    def average_score(
        self,
        reports: list[EvaluationReport],
    ) -> float:
        """
        Returns the average overall score across all reports.
        """

        if not reports:
            return 0.0

        return round(
            sum(report.overall_score for report in reports) / len(reports),
            2,
        )

    def pass_rate(
        self,
        reports: list[EvaluationReport],
    ) -> float:
        """
        Returns the percentage of reports that passed.
        """

        if not reports:
            return 0.0

        passed = sum(report.passed for report in reports)

        return round(
            passed / len(reports),
            2,
        )
