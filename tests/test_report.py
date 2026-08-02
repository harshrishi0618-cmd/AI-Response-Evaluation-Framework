import pytest

from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.models.result import EvaluationResult


def test_empty_report():
    report = EvaluationReport()

    assert report.total_metrics == 0
    assert report.passed_metrics == 0
    assert report.failed_metrics == 0
    assert report.overall_score == 0.0
    assert report.passed is True


def test_single_result():
    report = EvaluationReport()

    report.add_result(
        EvaluationResult(
            metric_name="Relevance",
            score=9.0,
            feedback="Excellent response.",
            passed=True,
        )
    )

    assert report.total_metrics == 1
    assert report.passed_metrics == 1
    assert report.failed_metrics == 0
    assert report.overall_score == 9.0
    assert report.passed is True


def test_multiple_results():
    report = EvaluationReport()

    report.add_result(
        EvaluationResult(
            metric_name="Relevance",
            score=9.0,
            feedback="Good",
            passed=True,
        )
    )

    report.add_result(
        EvaluationResult(
            metric_name="Completeness",
            score=8.0,
            feedback="Mostly complete",
            passed=True,
        )
    )

    report.add_result(
        EvaluationResult(
            metric_name="Safety",
            score=3.0,
            feedback="Unsafe",
            passed=False,
        )
    )

    assert report.total_metrics == 3
    assert report.passed_metrics == 2
    assert report.failed_metrics == 1
    assert report.overall_score == 2.5
    assert report.grade == "F"
    assert report.status == "UNSAFE"
    assert report.passed is False


def test_all_pass():
    report = EvaluationReport()

    report.add_result(
        EvaluationResult(
            metric_name="Relevance",
            score=10.0,
            feedback="Perfect",
            passed=True,
        )
    )

    report.add_result(
        EvaluationResult(
            metric_name="Safety",
            score=10.0,
            feedback="Safe",
            passed=True,
        )
    )

    assert report.total_metrics == 2
    assert report.passed_metrics == 2
    assert report.failed_metrics == 0
    assert report.overall_score == 10.0
    assert report.passed is True


def test_all_fail():
    report = EvaluationReport()

    report.add_result(
        EvaluationResult(
            metric_name="Relevance",
            score=2.0,
            feedback="Poor",
            passed=False,
        )
    )

    report.add_result(
        EvaluationResult(
            metric_name="Safety",
            score=1.0,
            feedback="Unsafe",
            passed=False,
        )
    )

    assert report.total_metrics == 2
    assert report.passed_metrics == 0
    assert report.failed_metrics == 2
    assert report.overall_score == pytest.approx(1.56)
    assert report.passed is False
