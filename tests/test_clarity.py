from ai_response_eval.evaluators.clarity import ClarityEvaluator
from ai_response_eval.models.request import EvaluationRequest


def test_clear_response():
    evaluator = ClarityEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response=(
            "Python is a programming language. It is easy to learn. It is widely used."
        ),
    )

    result = evaluator.evaluate(request)

    assert result.metric_name == "Clarity"
    assert result.score >= 8


def test_long_sentence():
    evaluator = ClarityEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response=(
            "Python is a programming language that has become one of the most "
            "popular languages in the world because it supports multiple paradigms "
            "and provides a huge collection of libraries while also remaining easy "
            "to learn for beginners."
        ),
    )

    result = evaluator.evaluate(request)

    assert result.score < 8


def test_repeated_words():
    evaluator = ClarityEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response="Python Python Python Python Python Python Python.",
    )

    result = evaluator.evaluate(request)

    assert result.score < 5


def test_empty_response():
    evaluator = ClarityEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response="",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0
    assert result.passed is False


def test_filler_words():
    evaluator = ClarityEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response=(
            "Basically, Python is actually really easy to learn and "
            "kind of useful for basically everything."
        ),
    )

    result = evaluator.evaluate(request)

    assert result.score < 8
