from __future__ import annotations

import json
from pathlib import Path

from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.reporting.summary import SummaryBuilder


class JSONReportGenerator:
    """
    Generates a JSON evaluation report.
    """

    @staticmethod
    def generate(report: EvaluationReport) -> dict:
        summary = SummaryBuilder.build(report)

        return {
            "overall_score": report.overall_score,
            "grade": summary.grade,
            "passed": report.passed,
            "pass_rate": report.pass_rate,
            "total_metrics": report.total_metrics,
            "passed_metrics": report.passed_metrics,
            "failed_metrics": report.failed_metrics,
            "strengths": summary.strengths,
            "weaknesses": summary.weaknesses,
            "recommendations": summary.recommendations,
            "executive_summary": summary.executive_summary,
            "metrics": [
                {
                    "metric": result.metric_name,
                    "score": result.score,
                    "percentage": result.percentage,
                    "passed": result.passed,
                    "feedback": result.feedback,
                }
                for result in report.results
            ],
        }

    @classmethod
    def save(
        cls,
        report: EvaluationReport,
        output_path: str | Path,
    ) -> None:
        output_path = Path(output_path)

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                cls.generate(report),
                f,
                indent=4,
                ensure_ascii=False,
            )
