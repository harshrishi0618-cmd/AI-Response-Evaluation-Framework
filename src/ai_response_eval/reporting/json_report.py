from __future__ import annotations

import json

from ai_response_eval.models.report import EvaluationReport


class JSONReportGenerator:
    """
    Generates a JSON representation of an evaluation report.
    """

    @staticmethod
    def generate(report: EvaluationReport) -> str:
        data = {
            "overall_score": report.overall_score,
            "passed_metrics": report.passed_metrics,
            "failed_metrics": report.failed_metrics,
            "pass_rate": report.pass_rate,
            "results": [],
        }

        for result in report.results:
            data["results"].append(
                {
                    "metric": result.metric_name,
                    "score": result.score,
                    "passed": result.passed,
                    "feedback": result.feedback,
                }
            )

        return json.dumps(data, indent=4)
