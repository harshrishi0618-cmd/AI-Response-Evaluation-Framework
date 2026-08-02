from __future__ import annotations

from html import escape
from pathlib import Path

from ai_response_eval.models.report import EvaluationReport
from ai_response_eval.reporting.summary import SummaryBuilder


class HTMLReportGenerator:
    """
    Generates a modern HTML evaluation report.
    """

    def generate(self, report: EvaluationReport) -> str:
        summary = SummaryBuilder.build(report)

        status = report.status

        if status == "PASSED":
            banner_color = "#22c55e"
            banner_bg = "#dcfce7"
        elif status == "REVIEW":
            banner_color = "#f59e0b"
            banner_bg = "#fef3c7"
        else:
            banner_color = "#ef4444"
            banner_bg = "#fee2e2"

        metric_cards = []

        for result in report.results:
            score = max(0.0, min(result.score, 10.0))
            percent = score * 10

            if score >= 8:
                metric_status = "PASS"
                color = "#22c55e"
            elif score >= 6:
                metric_status = "WARNING"
                color = "#f59e0b"
            else:
                metric_status = "FAIL"
                color = "#ef4444"

            metric_cards.append(
                f"""
<div class="metric-card">

<div class="metric-header">

<div class="metric-name">
{escape(result.metric_name)}
</div>

<div class="metric-status"
style="background:{color};">
{metric_status}
</div>

</div>

<div class="progress">

<div class="progress-fill"
style="
width:{percent:.0f}%;
background:{color};
">
</div>

</div>

<div class="metric-score">
{result.score:.1f}/10
</div>

<div class="metric-feedback">
{escape(result.feedback)}
</div>

</div>
"""
            )

        strengths = "".join(f"<li>{escape(item)}</li>" for item in summary.strengths)

        weaknesses = "".join(f"<li>{escape(item)}</li>" for item in summary.weaknesses)

        recommendations = "".join(
            f"<li>{escape(item)}</li>" for item in summary.recommendations
        )

        return f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
AI Response Evaluation Report
</title>

<style>

*{{
margin:0;
padding:0;
box-sizing:border-box;
}}

body{{
font-family:Inter,Segoe UI,Arial,sans-serif;
background:#eef2ff;
padding:40px;
color:#1e293b;
}}

.container{{
max-width:1300px;
margin:auto;
background:white;
border-radius:18px;
overflow:hidden;
box-shadow:
0 15px 45px rgba(0,0,0,.12);
}}

.header{{
background:linear-gradient(
135deg,
#2563eb,
#1d4ed8,
#312e81
);
padding:55px;
color:white;
}}

.header h1{{
font-size:38px;
font-weight:700;
}}

.header p{{
margin-top:12px;
opacity:.92;
font-size:18px;
}}

.summary-grid{{
display:grid;
grid-template-columns:
repeat(auto-fit,minmax(260px,1fr));
gap:25px;
padding:35px;
}}

.card{{
background:white;
border-radius:16px;
padding:28px;
box-shadow:
0 10px 25px rgba(0,0,0,.08);
}}

.card-title{{
font-size:14px;
text-transform:uppercase;
letter-spacing:1px;
color:#64748b;
margin-bottom:10px;
}}

.big-score{{
font-size:54px;
font-weight:700;
color:#2563eb;
}}

.grade{{
display:inline-block;
padding:8px 18px;
margin-top:12px;
background:#2563eb;
color:white;
border-radius:999px;
font-size:22px;
font-weight:700;
}}

.section{{
padding:35px;
}}

.section h2{{
font-size:28px;
margin-bottom:20px;
}}

.executive{{
background:#f8fafc;
border-left:6px solid #2563eb;
padding:25px;
border-radius:12px;
line-height:1.8;
font-size:17px;
}}

.status-banner{{
padding:28px;
margin:35px;
border-radius:18px;
font-size:20px;
font-weight:700;
text-align:center;
}}

.info-grid{{
display:grid;
grid-template-columns:
repeat(auto-fit,minmax(320px,1fr));
gap:30px;
margin-top:30px;
}}

.panel{{
background:#f8fafc;
padding:25px;
border-radius:16px;
}}

.panel h3{{
margin-bottom:18px;
}}

.panel ul{{
padding-left:20px;
}}

.panel li{{
margin-bottom:10px;
line-height:1.7;
}}

.metrics{{
display:grid;
grid-template-columns:
repeat(auto-fit,minmax(360px,1fr));
gap:25px;
margin-top:25px;
}}

.metric-card{{
background:white;
border-radius:18px;
padding:25px;
box-shadow:
0 8px 20px rgba(0,0,0,.08);
transition:.25s;
}}

.metric-card:hover{{
transform:translateY(-4px);
}}

.metric-header{{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:18px;
}}

.metric-name{{
font-size:22px;
font-weight:700;
}}

.metric-status{{
padding:6px 14px;
border-radius:999px;
font-size:13px;
font-weight:700;
color:white;
}}

.progress{{
height:14px;
background:#e5e7eb;
border-radius:999px;
overflow:hidden;
margin-bottom:15px;
}}

.progress-fill{{
height:100%;
border-radius:999px;
}}

.metric-score{{
font-size:26px;
font-weight:700;
margin-bottom:12px;
}}

.metric-feedback{{
color:#475569;
line-height:1.8;
font-size:15px;
}}

.charts{{
display:grid;
grid-template-columns:
repeat(auto-fit,minmax(500px,1fr));
gap:35px;
margin-top:25px;
}}

.chart-card{{
background:white;
padding:25px;
border-radius:18px;
box-shadow:
0 10px 22px rgba(0,0,0,.08);
min-height:380px;
display:flex;
justify-content:center;
align-items:center;
flex-direction:column;
}}

.chart-placeholder{{
width:100%;
height:280px;
display:flex;
justify-content:center;
align-items:center;
border:3px dashed #cbd5e1;
border-radius:16px;
font-size:18px;
color:#64748b;
background:#f8fafc;
}}

.footer{{
padding:35px;
background:#0f172a;
color:white;
text-align:center;
}}

.footer h3{{
margin-bottom:12px;
}}

.footer p{{
opacity:.85;
line-height:1.8;
}}

@media(max-width:900px){{

.summary-grid{{
grid-template-columns:1fr;
}}

.metrics{{
grid-template-columns:1fr;
}}

.charts{{
grid-template-columns:1fr;
}}

}}

</style>

</head>

<body>

<div class="container">

<div class="header">

<h1>
AI Response Evaluation Framework
</h1>

<p>
Professional AI Response Quality Assessment Report
</p>

</div>

<div class="summary-grid">

<div class="card">

<div class="card-title">
Evaluation Status
</div>

<div class="big-score">
{status}
</div>

<div class="grade">
Grade {summary.grade}
</div>

</div>

<div class="card">

<div class="card-title">
Metrics Passed
</div>

<div class="big-score">
{report.passed_metrics}/{report.total_metrics}
</div>

<div class="grade">
{report.pass_rate * 100:.0f}% PASS
</div>

</div>

<div class="card">

<div class="card-title">
Evaluation Status
</div>

<div class="big-score">
{"PASS" if report.passed else "FAIL"}
</div>

<div class="grade">
{"READY" if report.passed else "REVIEW"}
</div>

</div>

</div>

<div
class="status-banner"
style="
background:{banner_bg};
color:{banner_color};
border:3px solid {banner_color};
">

Evaluation Status: {status}

</div>

<div class="section">

<h2>
Executive Summary
</h2>

<div class="executive">

{escape(summary.executive_summary)}

</div>

<div class="info-grid">

<div class="panel">

<h3>
💪 Strengths
</h3>

<ul>

{strengths if strengths else "<li>No major strengths detected.</li>"}

</ul>

</div>

<div class="panel">

<h3>
⚠️ Weaknesses
</h3>

<ul>

{weaknesses if weaknesses else "<li>No significant weaknesses detected.</li>"}

</ul>

</div>

</div>

<div class="panel"
style="margin-top:30px;">

<h3>
💡 Recommendations
</h3>

<ul>

{recommendations if recommendations else "<li>No recommendations. Excellent overall response.</li>"}

</ul>

</div>

</div>

<div class="section">

<h2>
Metric Evaluation
</h2>

<div class="metrics">

{"".join(metric_cards)}

</div>

</div>

<div class="section">

<h2>
Performance Charts
</h2>

<div class="charts">

<div class="chart-card">

<h3>
Radar Chart
</h3>

<div class="chart-placeholder">

Radar Chart Placeholder

</div>

</div>

<div class="chart-card">

<h3>
Bar Chart
</h3>

<div class="chart-placeholder">

Bar Chart Placeholder

</div>

</div>

</div>

</div>

<div class="footer">

<h3>
AI Response Evaluation Framework
</h3>

<p>
Generated automatically by the AI Response Evaluation Framework.
</p>

<p>
Overall Score:
<strong>{summary.overall_score:.2f}/10</strong>
&nbsp;&nbsp;|&nbsp;&nbsp;
Grade:
<strong>{summary.grade}</strong>
&nbsp;&nbsp;|&nbsp;&nbsp;
Metrics Passed:
<strong>{report.passed_metrics}/{report.total_metrics}</strong>
</p>

</div>

</div>

</body>

</html>
"""

    def save(
        self,
        report: EvaluationReport,
        filepath: str | Path,
    ) -> None:
        """
        Save the generated HTML report to disk.
        """

        html = self.generate(report)

        path = Path(filepath)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            html,
            encoding="utf-8",
        )
