from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.models.result import EvaluationResult
from ai_response_eval.reporting.html_report import HTMLReportGenerator


def test_generate_html():
    report = EvaluationReport(
        results=[
            EvaluationResult(
                metric_name="Relevance",
                score=9,
                feedback="Good",
                passed=True,
            ),
            EvaluationResult(
                metric_name="Safety",
                score=10,
                feedback="Safe",
                passed=True,
            ),
        ]
    )

    generator = HTMLReportGenerator()

    html = generator.generate(report)

    assert "<html" in html.lower()
    assert "Relevance" in html
    assert "Safety" in html
    assert "Overall" in html
