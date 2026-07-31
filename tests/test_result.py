from ai_response_eval.models.result import EvaluationResult


def test_percentage():
    result = EvaluationResult(
        metric="Relevance",
        score=8,
        max_score=10,
    )

    assert result.percentage == 80.0


def test_passed():
    result = EvaluationResult(
        metric="Relevance",
        score=7,
        max_score=10,
    )

    assert result.passed is True


def test_failed():
    result = EvaluationResult(
        metric="Relevance",
        score=5,
        max_score=10,
    )

    assert result.passed is False
