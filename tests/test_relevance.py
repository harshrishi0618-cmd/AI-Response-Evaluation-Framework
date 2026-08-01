from ai_response_eval.evaluators.relevance import RelevanceEvaluator
from ai_response_eval.models.request import EvaluationRequest


def test_highly_relevant_response():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response="Machine learning is a field of AI.",
    )

    result = evaluator.evaluate(request)

    assert result.metric_name == "Relevance"
    assert result.score >= 0.6
    assert result.passed is True


def test_unrelated_response():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response="Paris is the capital of France.",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0
    assert result.passed is False


def test_partially_relevant_response():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning algorithms",
        response="Machine learning is useful.",
    )

    result = evaluator.evaluate(request)

    assert 0 < result.score < 10


def test_empty_prompt():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="",
        response="Machine learning is AI.",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0


def test_empty_response():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response="",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0
