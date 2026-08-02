from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.models.result import EvaluationResult
from ai_response_eval.reporting.json_report import JSONReportGenerator


def test_generate_json():
    report = EvaluationReport(
        results=[
            EvaluationResult(
                metric_name="Safety",
                score=10,
                feedback="Safe",
                passed=True,
            )
        ]
    )

    json_data = JSONReportGenerator.generate(report)

    assert isinstance(json_data, dict)

    assert json_data["overall_score"] == 10.0
    assert json_data["grade"] == "A+"
    assert json_data["passed_metrics"] == 1
    assert json_data["failed_metrics"] == 0

    assert len(json_data["metrics"]) == 1

    metric = json_data["metrics"][0]

    assert metric["metric"] == "Safety"
    assert metric["score"] == 10
    assert metric["passed"] is True
    assert metric["feedback"] == "Safe"
