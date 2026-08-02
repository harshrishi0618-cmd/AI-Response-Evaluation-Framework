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
            metric_name="Dummy",
            score=10.0,
            feedback="Everything looks good.",
            passed=True,
        )


def test_engine_pipeline():
    request = EvaluationRequest(
        prompt="Explain AI",
        response="AI stands for Artificial Intelligence.",
    )

    engine = EvaluationEngine(
        evaluators=[DummyEvaluator()],
    )

    report = engine.evaluate(request)

    assert len(report.results) == 1
    assert report.results[0].metric_name == "Dummy"

    assert report.total_metrics == 1
    assert report.passed_metrics == 1
    assert report.failed_metrics == 0

    assert report.overall_score == 10.0
    assert report.passed is True
