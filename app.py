from __future__ import annotations

import tempfile

import pandas as pd
import streamlit as st

from ai_response_eval.batch.evaluator import BatchEvaluator
from ai_response_eval.batch.io import BatchExporter, BatchLoader
from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.evaluators.clarity import ClarityEvaluator
from ai_response_eval.evaluators.completeness import CompletenessEvaluator
from ai_response_eval.evaluators.conciseness import ConcisenessEvaluator
from ai_response_eval.evaluators.relevance import RelevanceEvaluator
from ai_response_eval.evaluators.safety import SafetyEvaluator
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.reporting.html_report import HTMLReportGenerator
from ai_response_eval.reporting.json_report import JSONReportGenerator
from ai_response_eval.visualization.charts import DashboardCharts

st.set_page_config(
    page_title="AI Response Evaluation Framework",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Response Evaluation Framework")
st.write("Evaluate AI-generated responses using multiple quality metrics.")

engine = EvaluationEngine(
    evaluators=[
        RelevanceEvaluator(),
        CompletenessEvaluator(),
        ClarityEvaluator(),
        SafetyEvaluator(),
        ConcisenessEvaluator(),
    ]
)

# =====================================================
# SINGLE EVALUATION
# =====================================================

st.header("📝 Single Response Evaluation")

prompt = st.text_area(
    "Prompt",
    placeholder="Enter the user's prompt...",
    height=150,
)

response = st.text_area(
    "AI Response",
    placeholder="Enter the AI response...",
    height=250,
)

if st.button("Evaluate Response", use_container_width=True):
    if not prompt.strip() or not response.strip():
        st.error("Please provide both a prompt and a response.")
        st.stop()

    report = engine.evaluate(
        EvaluationRequest(
            prompt=prompt,
            response=response,
        )
    )

    st.divider()

    st.header("📊 Evaluation Results")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Overall Score", f"{report.overall_score:.2f}/10")
    c2.metric("Passed", report.passed_metrics)
    c3.metric("Failed", report.failed_metrics)
    c4.metric("Pass Rate", f"{report.pass_rate * 100:.0f}%")

    st.divider()

    for result in report.results:
        st.markdown(f"### {result.metric_name}")

        st.progress(result.score / 10)

        left, right = st.columns([1, 5])

        with left:
            st.metric("Score", f"{result.score:.1f}/10")

        with right:
            if result.passed:
                st.success(f"✅ {result.feedback}")
            else:
                st.error(f"❌ {result.feedback}")

        st.divider()

    st.header("📈 Analytics")

    chart1, chart2 = st.columns(2)

    with chart1:
        st.plotly_chart(
            DashboardCharts.radar_chart(report),
            use_container_width=True,
        )

    with chart2:
        st.plotly_chart(
            DashboardCharts.bar_chart(report),
            use_container_width=True,
        )

    st.divider()

    st.header("📥 Export Reports")

    html_report = HTMLReportGenerator().generate(report)
    json_report = JSONReportGenerator().generate(report)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "📄 Download HTML Report",
            html_report,
            file_name="evaluation_report.html",
            mime="text/html",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "📄 Download JSON Report",
            json_report,
            file_name="evaluation_report.json",
            mime="application/json",
            use_container_width=True,
        )

# =====================================================
# BATCH EVALUATION
# =====================================================

st.divider()

st.header("📂 Batch Evaluation")

uploaded_file = st.file_uploader(
    "Upload CSV (columns: prompt,response)",
    type="csv",
)

if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)

    st.success(f"Loaded {len(dataframe)} records")

    st.dataframe(
        dataframe,
        use_container_width=True,
    )

    if st.button(
        "🚀 Evaluate Dataset",
        use_container_width=True,
    ):
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv",
        ) as tmp:
            dataframe.to_csv(
                tmp.name,
                index=False,
            )

            requests = BatchLoader.load_csv(tmp.name)

        reports = BatchEvaluator(engine).evaluate(requests)

        rows = []

        for index, report in enumerate(reports, start=1):
            row = {
                "Example": index,
                "Overall": report.overall_score,
            }

            for result in report.results:
                row[result.metric_name] = result.score

            rows.append(row)

        results_df = pd.DataFrame(rows)

        st.subheader("Batch Results")

        st.dataframe(
            results_df,
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
        ) as file:
            st.download_button(
                "⬇ Download Evaluated CSV",
                file,
                file_name="results.csv",
                mime="text/csv",
                use_container_width=True,
            )

st.divider()

st.caption("AI Response Evaluation Framework • Built with Streamlit, Plotly & FastAPI")
