from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult


class DummyEvaluator(BaseEvaluator):
    @property
    def metric_name(self) -> str:
        return "Dummy"

    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:
        return EvaluationResult(
            metric="Dummy",
            score=10,
            max_score=10,
        )


def test_engine_runs_all_evaluators():
    engine = EvaluationEngine(evaluators=[DummyEvaluator()])

    report = engine.evaluate(
        prompt="Hello",
        response="Hi",
    )

    assert report.total_metrics == 1
    assert report.overall_score == 100.0
    assert report.passed is True
