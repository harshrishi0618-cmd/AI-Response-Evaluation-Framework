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

    assert "Safety" in json_data
    assert "overall_score" in json_data
