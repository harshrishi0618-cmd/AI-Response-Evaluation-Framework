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
            metric_name="Relevance",
            score=0.8,
            feedback="Good",
            passed=True,
        )
    )

    report.add_result(
        EvaluationResult(
            metric_name="Clarity",
            score=0.6,
            feedback="Needs work",
            passed=False,
        )
    )

    assert report.total_metrics == 2
    assert report.passed_metrics == 1
    assert report.failed_metrics == 1
    assert report.overall_score == 0.7
    assert report.passed is False
