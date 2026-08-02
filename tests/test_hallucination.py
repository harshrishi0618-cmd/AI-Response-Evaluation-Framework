from ai_response_eval.evaluators.hallucination import HallucinationEvaluator
from ai_response_eval.models.request import EvaluationRequest


def test_supported_response():
    evaluator = HallucinationEvaluator()

    request = EvaluationRequest(
        prompt="What is Python?",
        response=(
            "Python is a high-level programming language used "
            "for software development, automation, and AI."
        ),
    )

    result = evaluator.evaluate(request)

    assert result.metric_name == "Hallucination"
    assert result.score >= 8
    assert result.passed is True


def test_unrelated_response():
    evaluator = HallucinationEvaluator()

    request = EvaluationRequest(
        prompt="What is Python?",
        response="The Eiffel Tower is located in Paris.",
    )

    result = evaluator.evaluate(request)

    assert result.score < 7
    assert result.passed is False


def test_suspicious_factual_claim():
    """
    The evaluator estimates hallucination risk.
    It does NOT verify facts against an external
    knowledge source.
    """

    evaluator = HallucinationEvaluator()

    request = EvaluationRequest(
        prompt="What is Python?",
        response="Python was invented by Elon Musk in 2024.",
    )

    result = evaluator.evaluate(request)

    assert result.score <= 7
    assert result.passed is False


def test_multiple_suspicious_claims():
    evaluator = HallucinationEvaluator()

    request = EvaluationRequest(
        prompt="Tell me about France.",
        response=(
            "France was invented by John Doe in 2022. "
            "Its capital was founded by Elon Musk."
        ),
    )

    result = evaluator.evaluate(request)

    assert result.score <= 5
    assert result.passed is False


def test_hedging_language():
    evaluator = HallucinationEvaluator()

    request = EvaluationRequest(
        prompt="Who discovered Atlantis?",
        response=("Atlantis may have existed, but historians are not sure."),
    )

    result = evaluator.evaluate(request)

    assert result.score >= 7


def test_absolute_certainty():
    evaluator = HallucinationEvaluator()

    request = EvaluationRequest(
        prompt="Who discovered Atlantis?",
        response=("Atlantis definitely existed and this proves it."),
    )

    result = evaluator.evaluate(request)

    assert result.score <= 6


def test_empty_response():
    evaluator = HallucinationEvaluator()

    request = EvaluationRequest(
        prompt="Explain Python.",
        response="",
    )

    result = evaluator.evaluate(request)

    assert result.score == 0
    assert result.passed is False
