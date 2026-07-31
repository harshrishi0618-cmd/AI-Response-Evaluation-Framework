from __future__ import annotations

from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.models.request import EvaluationRequest


class EvaluationEngine:
    """
    Runs all registered evaluators.
    """

    def __init__(self, evaluators: list[BaseEvaluator]) -> None:
        self.evaluators = evaluators

    def evaluate(
        self,
        prompt: str,
        response: str,
    ) -> EvaluationReport:

        request = EvaluationRequest(
            prompt=prompt,
            response=response,
        )

        report = EvaluationReport()

        for evaluator in self.evaluators:
            result = evaluator.evaluate(request)
            report.add_result(result)

        return report
