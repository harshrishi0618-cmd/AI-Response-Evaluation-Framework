from ai_response_eval.evaluators.conciseness import ConcisenessEvaluator
from ai_response_eval.models.request import EvaluationRequest


def test_concise_response():
    evaluator = ConcisenessEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response="Python is an easy-to-learn programming language.",
    )

    result = evaluator.evaluate(request)

    assert result.metric_name == "Conciseness"
    assert result.score >= 8
    assert result.passed is True


def test_repeated_words():
    evaluator = ConcisenessEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response="Python Python Python Python Python.",
    )

    result = evaluator.evaluate(request)

    assert result.score < 6


def test_filler_words():
    evaluator = ConcisenessEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response=(
            "Basically, Python is actually really very kind of extremely easy to learn."
        ),
    )

    result = evaluator.evaluate(request)

    assert result.score < 8


def test_empty_response():
    evaluator = ConcisenessEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response="",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0
    assert result.passed is False


def test_repeated_sentence():
    evaluator = ConcisenessEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python",
        response=("Python is easy. Python is easy. Python is easy."),
    )

    result = evaluator.evaluate(request)

    assert result.score < 6
