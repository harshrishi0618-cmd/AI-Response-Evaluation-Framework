from html import escape
from pathlib import Path

from ai_response_eval.models.report import EvaluationReport


class HTMLReportGenerator:
    """
    Generates an HTML report from an EvaluationReport.
    """

    def generate(self, report: EvaluationReport) -> str:
        rows = []

        for result in report.results:
            rows.append(
                f"""
                <tr>
                    <td>{escape(result.metric_name)}</td>
                    <td>{result.score:.1f}</td>
                    <td>{escape(result.feedback)}</td>
                </tr>
                """
            )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Response Evaluation Report</title>

<style>
body {{
    font-family: Arial, Helvetica, sans-serif;
    background: #f4f4f4;
    margin: 40px;
}}

.container {{
    max-width: 900px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,.15);
}}

h1 {{
    text-align: center;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}}

th,
td {{
    border: 1px solid #ddd;
    padding: 10px;
}}

th {{
    background: #2f80ed;
    color: white;
}}

.score {{
    margin-top: 25px;
    font-size: 22px;
    font-weight: bold;
}}
</style>

</head>

<body>

<div class="container">

<h1>AI Response Evaluation Report</h1>

<table>

<tr>
<th>Metric</th>
<th>Score</th>
<th>Feedback</th>
</tr>

{"".join(rows)}

</table>

<div class="score">
Overall Score: {report.overall_score:.2f}
</div>

</div>

</body>

</html>
"""

    def save(self, report: EvaluationReport, filepath: str | Path) -> None:
        """
        Save the generated HTML report to disk.
        """
        html = self.generate(report)

        path = Path(filepath)
        path.write_text(html, encoding="utf-8")
