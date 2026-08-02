from pathlib import Path

from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.evaluators.relevance import RelevanceEvaluator
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.reporting.html_report import HTMLReportGenerator


def test_full_report_pipeline(tmp_path: Path):
    engine = EvaluationEngine(
        evaluators=[
            RelevanceEvaluator(),
        ]
    )

    request = EvaluationRequest(
        prompt="Explain Python",
        response="Python is a programming language.",
    )

    report = engine.evaluate(request)

    generator = HTMLReportGenerator()

    output_file = tmp_path / "evaluation_report.html"

    generator.save(report, output_file)

    assert output_file.exists()

    html = output_file.read_text(encoding="utf-8")

    assert "Relevance" in html
    assert "Overall Score" in html
