from ai_response_eval.models.result import EvaluationResult


def test_percentage_full_score():
    result = EvaluationResult(
        metric_name="Relevance",
        score=10.0,
        feedback="Excellent",
        passed=True,
    )

    assert result.percentage == 100.0


def test_percentage_partial_score():
    result = EvaluationResult(
        metric_name="Relevance",
        score=8.5,
        feedback="Good",
        passed=True,
    )

    assert result.percentage == 85.0


def test_percentage_zero_score():
    result = EvaluationResult(
        metric_name="Relevance",
        score=0.0,
        feedback="Poor",
        passed=False,
    )

    assert result.percentage == 0.0


def test_passed():
    result = EvaluationResult(
        metric_name="Safety",
        score=9.0,
        feedback="Safe",
        passed=True,
    )

    assert result.passed is True


def test_failed():
    result = EvaluationResult(
        metric_name="Safety",
        score=3.0,
        feedback="Unsafe",
        passed=False,
    )

    assert result.passed is False
