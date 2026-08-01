from pathlib import Path

from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.models.result import EvaluationResult
from ai_response_eval.reporting.html_report import HTMLReportGenerator


def test_save_html(tmp_path: Path):
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

    output_file = tmp_path / "report.html"

    generator = HTMLReportGenerator()
    generator.save(report, output_file)

    assert output_file.exists()

    html = output_file.read_text()

    assert "<html" in html.lower()
    assert "Safety" in html
