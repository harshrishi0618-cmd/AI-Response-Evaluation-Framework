from __future__ import annotations

import plotly.graph_objects as go

from ai_response_eval.models.report import EvaluationReport


class DashboardCharts:
    """
    Creates Plotly charts for the dashboard.
    """

    @staticmethod
    def radar_chart(report: EvaluationReport):
        labels = [result.metric_name for result in report.results]
        scores = [result.score for result in report.results]

        labels.append(labels[0])
        scores.append(scores[0])

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=scores,
                theta=labels,
                fill="toself",
                name="Evaluation",
            )
        )

        fig.update_layout(
            polar={
                "radialaxis": {
                    "visible": True,
                    "range": [0, 10],
                }
            },
            showlegend=False,
            margin={
                "l": 40,
                "r": 40,
                "t": 40,
                "b": 40,
            },
            height=500,
        )

        return fig

    @staticmethod
    def bar_chart(report: EvaluationReport):
        labels = [result.metric_name for result in report.results]
        scores = [result.score for result in report.results]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=labels,
                y=scores,
            )
        )

        fig.update_layout(
            yaxis={
                "range": [0, 10],
            },
            height=450,
            margin={
                "l": 40,
                "r": 40,
                "t": 40,
                "b": 40,
            },
        )

        return fig
