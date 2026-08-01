from ai_response_eval.models.result import EvaluationResult


def test_percentage():
    result = EvaluationResult(
        metric_name="Relevance",
        score=0.8,
        feedback="Good",
        passed=True,
    )

    assert result.percentage == 80.0


def test_passed():
    result = EvaluationResult(
        metric_name="Relevance",
        score=0.7,
        feedback="Good",
        passed=True,
    )

    assert result.passed is True


def test_failed():
    result = EvaluationResult(
        metric_name="Relevance",
        score=0.5,
        feedback="Poor",
        passed=False,
    )

    assert result.passed is False
