from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult


class DummyEvaluator(BaseEvaluator):
    """Simple evaluator used only for testing."""

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        return EvaluationResult(
            metric_name="Dummy",
            score=1.0,
            feedback="Everything looks good.",
            passed=True,
        )


def test_engine_pipeline():
    request = EvaluationRequest(
        prompt="Explain AI", response="AI is Artificial Intelligence."
    )

    engine = EvaluationEngine(evaluators=[DummyEvaluator()])

    report = engine.evaluate(request)

    assert report.overall_score == 1.0
    assert report.passed is True
    assert len(report.results) == 1
    assert report.results[0].metric_name == "Dummy"
