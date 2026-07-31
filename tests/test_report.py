from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.models.result import EvaluationResult


def test_empty_report():
    report = EvaluationReport()

    assert report.total_metrics == 0
    assert report.overall_score == 0.0
    assert report.passed is True


def test_report_statistics():
    report = EvaluationReport()

    report.add_result(
        EvaluationResult(
            metric="Relevance",
            score=8,
            max_score=10,
        )
    )

    report.add_result(
        EvaluationResult(
            metric="Clarity",
            score=6,
            max_score=10,
        )
    )

    assert report.total_metrics == 2
    assert report.passed_metrics == 1
    assert report.failed_metrics == 1
    assert report.overall_score == 70.0
    assert report.passed is False
