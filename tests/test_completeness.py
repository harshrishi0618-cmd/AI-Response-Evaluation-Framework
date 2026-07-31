from ai_response_eval.evaluators.completeness import CompletenessEvaluator
from ai_response_eval.models.request import EvaluationRequest


def test_complete_response():
    evaluator = CompletenessEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response=(
            "Machine learning is a branch of artificial intelligence "
            "that learns patterns from data."
        ),
    )

    result = evaluator.evaluate(request)

    assert result.metric == "Completeness"
    assert result.score >= 9
    assert result.passed is True


def test_short_response():
    evaluator = CompletenessEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response="Machine learning.",
    )

    result = evaluator.evaluate(request)

    assert result.score < 9


def test_unrelated_response():
    evaluator = CompletenessEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response="Paris is the capital of France.",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0
    assert result.passed is False


def test_empty_prompt():
    evaluator = CompletenessEvaluator()

    request = EvaluationRequest(
        prompt="",
        response="Machine learning is AI.",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0


def test_empty_response():
    evaluator = CompletenessEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response="",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0
