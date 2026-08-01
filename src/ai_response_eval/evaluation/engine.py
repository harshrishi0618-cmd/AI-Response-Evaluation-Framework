from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.models.request import EvaluationRequest


class EvaluationEngine:
    """
    Coordinates all evaluators and produces a final evaluation report.
    """

    def __init__(self, evaluators: list[BaseEvaluator]):
        if not evaluators:
            raise ValueError("EvaluationEngine requires at least one evaluator.")

        self.evaluators = evaluators

    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationReport:
        """
        Run all evaluators and generate a report.
        """

        report = EvaluationReport()

        for evaluator in self.evaluators:
            result = evaluator.evaluate(request)
            report.add_result(result)

        return report
