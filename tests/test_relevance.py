from ai_response_eval.evaluators.relevance import RelevanceEvaluator
from ai_response_eval.models.request import EvaluationRequest


def test_highly_relevant_response():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response=(
            "Machine learning is a branch of artificial intelligence "
            "that enables computers to learn from data."
        ),
    )

    result = evaluator.evaluate(request)

    assert result.metric_name == "Relevance"
    assert result.score >= 8
    assert result.passed is True


def test_partially_relevant_response():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning algorithms",
        response="Machine learning is useful.",
    )

    result = evaluator.evaluate(request)

    assert 4 <= result.score < 8


def test_unrelated_response():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response="Pizza tastes good.",
    )

    result = evaluator.evaluate(request)

    assert result.score <= 2
    assert result.passed is False


def test_relevant_but_factually_wrong():
    """
    Relevance should remain high because the response
    discusses the requested topic.

    HallucinationEvaluator is responsible for
    factual correctness.
    """

    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="What is Python?",
        response="Python was invented by Elon Musk.",
    )

    result = evaluator.evaluate(request)

    assert result.score >= 7
    assert result.passed is True


def test_empty_prompt():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="",
        response="Machine learning is AI.",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0
    assert result.passed is False


def test_empty_response():
    evaluator = RelevanceEvaluator()

    request = EvaluationRequest(
        prompt="Explain machine learning",
        response="",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0
    assert result.passed is False
