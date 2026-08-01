from __future__ import annotations

import csv
from pathlib import Path

from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.models.request import EvaluationRequest


class BatchLoader:
    """
    Loads prompt-response pairs from CSV files.
    """

    @staticmethod
    def load_csv(path: str | Path) -> list[EvaluationRequest]:
        requests: list[EvaluationRequest] = []

        with open(path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError("CSV file is empty.")

            required = {"prompt", "response"}

            if not required.issubset(set(reader.fieldnames)):
                raise ValueError("CSV must contain 'prompt' and 'response' columns.")

            for row in reader:
                requests.append(
                    EvaluationRequest(
                        prompt=row["prompt"],
                        response=row["response"],
                    )
                )

        return requests


class BatchExporter:
    """
    Exports evaluation reports to CSV.
    """

    @staticmethod
    def save_csv(
        reports: list[EvaluationReport],
        path: str | Path,
    ) -> None:

        if not reports:
            raise ValueError("No reports to export.")

        metric_names = [result.metric_name for result in reports[0].results]

        headers = [
            "example",
            "overall_score",
            *metric_names,
        ]

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            writer.writerow(headers)

            for index, report in enumerate(
                reports,
                start=1,
            ):
                row = [
                    index,
                    report.overall_score,
                ]

                row.extend(result.score for result in report.results)

                writer.writerow(row)
