from __future__ import annotations

import tempfile

import pandas as pd
import plotly.express as px
import streamlit as st

from ai_response_eval.batch.evaluator import BatchEvaluator
from ai_response_eval.batch.io import BatchExporter, BatchLoader
from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.evaluators.clarity import ClarityEvaluator
from ai_response_eval.evaluators.completeness import CompletenessEvaluator
from ai_response_eval.evaluators.conciseness import ConcisenessEvaluator
from ai_response_eval.evaluators.hallucination import HallucinationEvaluator
from ai_response_eval.evaluators.prompt_security import PromptSecurityEvaluator
from ai_response_eval.evaluators.relevance import RelevanceEvaluator
from ai_response_eval.evaluators.safety import SafetyEvaluator
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.reporting.html_report import HTMLReportGenerator
from ai_response_eval.reporting.json_report import JSONReportGenerator
from ai_response_eval.reporting.summary import SummaryBuilder
from ai_response_eval.visualization.charts import DashboardCharts

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Response Evaluation Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{
padding-top:2rem;
padding-bottom:2rem;
max-width:1450px;
}

.main-title{
font-size:3rem;
font-weight:800;
color:#2563eb;
margin-bottom:0;
}

.sub-title{
color:#64748b;
font-size:1.1rem;
margin-bottom:2rem;
}

.metric-card{
background:white;
border-radius:18px;
padding:22px;
box-shadow:0 8px 25px rgba(0,0,0,.08);
border:1px solid #e5e7eb;
}

.metric-value{
font-size:2.5rem;
font-weight:700;
color:#2563eb;
}

.metric-label{
color:#64748b;
font-size:.95rem;
}

.grade-card{
background:linear-gradient(
135deg,
#2563eb,
#1d4ed8
);
border-radius:18px;
padding:22px;
color:white;
text-align:center;
box-shadow:0 10px 30px rgba(37,99,235,.3);
}

.grade-text{
font-size:3rem;
font-weight:800;
}

.section-card{
background:white;
border-radius:18px;
padding:24px;
box-shadow:0 6px 18px rgba(0,0,0,.08);
border:1px solid #e5e7eb;
margin-bottom:20px;
}

.section-title{
font-size:1.4rem;
font-weight:700;
margin-bottom:18px;
color:#1e293b;
}

.summary-box{
background:#f8fafc;
padding:20px;
border-left:6px solid #2563eb;
border-radius:12px;
line-height:1.8;
}

.good{
color:#16a34a;
font-weight:600;
}

.bad{
color:#dc2626;
font-weight:600;
}

.metric-box{
padding:18px;
background:#f8fafc;
border-radius:14px;
margin-bottom:15px;
border:1px solid #e2e8f0;
}

.metric-name{
font-size:1.2rem;
font-weight:700;
margin-bottom:8px;
}

.footer{
margin-top:60px;
text-align:center;
color:#94a3b8;
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/openai.svg",
        width=60,
    )

    st.title("AI Response Eval")

    page = st.radio(
        "Navigation",
        [
            "Single Evaluation",
            "Batch Evaluation",
        ],
    )

    st.divider()

    st.markdown(
        """
### Framework

✅ Relevance

✅ Completeness

✅ Clarity

✅ Safety

✅ Conciseness

✅ Hallucination
"""
    )

    st.divider()

    st.caption("Version 1.0")

# ============================================================
# ENGINE
# ============================================================

engine = EvaluationEngine(
    evaluators=[
        RelevanceEvaluator(),
        CompletenessEvaluator(),
        ClarityEvaluator(),
        SafetyEvaluator(),
        ConcisenessEvaluator(),
        HallucinationEvaluator(),
        PromptSecurityEvaluator(),
    ]
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="main-title">
🤖 AI Response Evaluation Framework
</div>

<div class="sub-title">
Professional evaluation of AI generated responses using
semantic similarity, safety analysis, hallucination
detection and quality metrics.
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SINGLE EVALUATION
# ============================================================

if page == "Single Evaluation":
    st.markdown("## ✍️ Evaluate Response")

    prompt = st.text_area(
        "Prompt",
        height=160,
        placeholder="Enter the user's prompt...",
    )

    response = st.text_area(
        "AI Response",
        height=240,
        placeholder="Enter the AI response...",
    )

    evaluate = st.button(
        "🚀 Evaluate",
        use_container_width=True,
        type="primary",
    )

    if evaluate:
        if not prompt.strip():
            st.error("Prompt cannot be empty.")
            st.stop()

        if not response.strip():
            st.error("Response cannot be empty.")
            st.stop()

        with st.spinner("Evaluating response..."):
            report = engine.evaluate(
                EvaluationRequest(
                    prompt=prompt,
                    response=response,
                )
            )

            summary = SummaryBuilder.build(report)

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
<div class="metric-card">

<div class="metric-label">
Overall Score
</div>

<div class="metric-value">
{report.overall_score:.2f}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

        with c2:
            status_colors = {
                "PASSED": "🟢",
                "REVIEW": "🟡",
                "UNSAFE": "🔴",
            }

            st.markdown(
                f"""
<div class="grade-card">

Status

<div class="grade-text">

{status_colors[report.status]} {report.status}

</div>

<br>

<b>Grade:</b> {report.grade}

</div>
""",
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
<div class="metric-card">

<div class="metric-label">

Passed Metrics

</div>

<div class="metric-value">

{report.passed_metrics}

</div>

</div>
""",
                unsafe_allow_html=True,
            )

        with c4:
            st.markdown(
                f"""
<div class="metric-card">

<div class="metric-label">

Pass Rate

</div>

<div class="metric-value">

{report.pass_rate * 100:.0f}%

</div>

</div>
""",
                unsafe_allow_html=True,
            )

        st.write("")

        left, right = st.columns([2, 1])

        with left:
            st.markdown(
                """
<div class="section-card">

<div class="section-title">

Executive Summary

</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
<div class="summary-box">

{summary.executive_summary}

</div>

</div>
""",
                unsafe_allow_html=True,
            )

        with right:
            st.markdown(
                """
<div class="section-card">

<div class="section-title">

Quick Overview

</div>
""",
                unsafe_allow_html=True,
            )

            st.metric(
                "Metrics",
                report.total_metrics,
            )

            st.metric(
                "Failed",
                report.failed_metrics,
            )

            st.metric(
                "Status",
                "PASS" if report.passed else "REVIEW",
            )

            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(
                """
<div class="section-card">

<div class="section-title">
💪 Strengths
</div>
""",
                unsafe_allow_html=True,
            )

            if summary.strengths:
                for strength in summary.strengths:
                    st.success(strength)

            else:
                st.info("No significant strengths identified.")

            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown(
                """
<div class="section-card">

<div class="section-title">
⚠️ Weaknesses
</div>
""",
                unsafe_allow_html=True,
            )

            if summary.weaknesses:
                for weakness in summary.weaknesses:
                    st.warning(weakness)

            else:
                st.success("No significant weaknesses detected.")

            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        st.markdown(
            """
<div class="section-card">

<div class="section-title">
💡 Recommendations
</div>
""",
            unsafe_allow_html=True,
        )

        if summary.recommendations:
            for recommendation in summary.recommendations:
                st.info(recommendation)

        else:
            st.success("Excellent response. No recommendations generated.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        st.markdown(
            """
<div class="section-card">

<div class="section-title">
📊 Metric Breakdown
</div>
""",
            unsafe_allow_html=True,
        )

        for result in report.results:
            score = result.score

            if score >= 8:
                color = "#22c55e"

            elif score >= 6:
                color = "#f59e0b"

            else:
                color = "#ef4444"

            st.markdown(
                f"""
<div class="metric-box">

<div class="metric-name">

{result.metric_name}

</div>

<div style="margin-bottom:10px;">

<b>{score:.1f}/10</b>

</div>

<div style="
background:#e5e7eb;
height:14px;
border-radius:999px;
overflow:hidden;
">

<div style="
width:{score * 10:.0f}%;
height:14px;
background:{color};
">
</div>

</div>

<div style="
margin-top:12px;
color:#475569;
line-height:1.7;
">

{result.feedback}

</div>

</div>
""",
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        st.markdown("## 📈 Analytics")

        chart_left, chart_right = st.columns(2)

        with chart_left:
            radar = DashboardCharts.radar_chart(report)

            radar.update_layout(
                height=500,
                margin={
                    "l": 20,
                    "r": 20,
                    "t": 40,
                    "b": 20,
                },
            )

            st.plotly_chart(
                radar,
                use_container_width=True,
            )

        with chart_right:
            bar = DashboardCharts.bar_chart(report)

            bar.update_layout(
                height=500,
                margin={
                    "l": 20,
                    "r": 20,
                    "t": 40,
                    "b": 20,
                },
            )

            st.plotly_chart(
                bar,
                use_container_width=True,
            )

            st.write("")

        st.markdown("## 📥 Export Reports")

        import json

        html_report = HTMLReportGenerator().generate(report)

        json_report = json.dumps(
            JSONReportGenerator.generate(report),
            indent=4,
            ensure_ascii=False,
        )

        export1, export2 = st.columns(2)

        with export1:
            st.download_button(
                label="📄 Download HTML Report",
                data=html_report,
                file_name="evaluation_report.html",
                mime="text/html",
                use_container_width=True,
            )

        with export2:
            st.download_button(
                label="📄 Download JSON Report",
                data=json_report,
                file_name="evaluation_report.json",
                mime="application/json",
                use_container_width=True,
            )

# ============================================================
# BATCH EVALUATION
# ============================================================

elif page == "Batch Evaluation":
    st.markdown("## 📂 Batch Evaluation")

    st.info("Upload a CSV file containing **prompt** and **response** columns.")

    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=["csv"],
    )

    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)

        st.success(f"Loaded **{len(dataframe)}** evaluation samples.")

        preview_col1, preview_col2 = st.columns([3, 1])

        with preview_col1:
            st.dataframe(
                dataframe,
                use_container_width=True,
                height=350,
            )

        with preview_col2:
            st.metric(
                "Rows",
                len(dataframe),
            )

            st.metric(
                "Columns",
                len(dataframe.columns),
            )

            st.metric(
                "Required",
                "prompt,response",
            )

        st.write("")

        if st.button(
            "🚀 Evaluate Entire Dataset",
            use_container_width=True,
            type="primary",
        ):
            progress = st.progress(0)

            status = st.empty()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".csv",
            ) as tmp:
                dataframe.to_csv(
                    tmp.name,
                    index=False,
                )

                requests = BatchLoader.load_csv(tmp.name)

            reports = []

            total = len(requests)

            evaluator = BatchEvaluator(engine)

            for i, request in enumerate(requests):
                reports.append(engine.evaluate(request))

                progress.progress((i + 1) / total)

                status.info(f"Evaluating {i + 1}/{total}")

            status.success("Evaluation completed.")

            rows = []

            for index, report in enumerate(
                reports,
                start=1,
            ):
                row = {
                    "Example": index,
                    "Overall Score": report.overall_score,
                    "Passed": report.passed,
                }

                for result in report.results:
                    row[result.metric_name] = result.score

                rows.append(row)

            results_df = pd.DataFrame(rows)

            st.write("")

            st.markdown("## 📈 Batch Results")

            st.dataframe(
                results_df,
                use_container_width=True,
                height=450,
            )

            st.write("")

            avg_score = round(
                results_df["Overall Score"].mean(),
                2,
            )

            passed = int(results_df["Passed"].sum())

            failed = len(results_df) - passed

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Average Score",
                avg_score,
            )

            c2.metric(
                "Passed",
                passed,
            )

            c3.metric(
                "Failed",
                failed,
            )

            st.write("")

            metric_columns = [
                col
                for col in results_df.columns
                if col
                not in (
                    "Example",
                    "Overall Score",
                    "Passed",
                )
            ]

            metric_average = results_df[metric_columns].mean().reset_index()

            metric_average.columns = [
                "Metric",
                "Average",
            ]

            fig = px.bar(
                metric_average,
                x="Metric",
                y="Average",
                text="Average",
                title="Average Metric Scores",
            )

            fig.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside",
            )

            fig.update_layout(
                height=500,
                xaxis_title="",
                yaxis_title="Average Score",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            output_path = "examples/results.csv"

            BatchExporter.save_csv(
                reports,
                output_path,
            )

            with open(
                output_path,
                "rb",
            ) as f:
                st.download_button(
                    "⬇ Download Evaluated CSV",
                    f,
                    file_name="evaluation_results.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

st.markdown("---")

st.markdown(
    """
<div class="footer">

<b>AI Response Evaluation Framework v1.0</b>

<br><br>

Built with ❤️ using

Python • Streamlit • Plotly • FastAPI •
Sentence Transformers

</div>
""",
    unsafe_allow_html=True,
)
