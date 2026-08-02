from fastapi import FastAPI

from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.evaluators.clarity import ClarityEvaluator
from ai_response_eval.evaluators.completeness import CompletenessEvaluator
from ai_response_eval.evaluators.conciseness import ConcisenessEvaluator
from ai_response_eval.evaluators.hallucination import HallucinationEvaluator
from ai_response_eval.evaluators.prompt_security import PromptSecurityEvaluator
from ai_response_eval.evaluators.relevance import RelevanceEvaluator
from ai_response_eval.evaluators.safety import SafetyEvaluator
from ai_response_eval.models.request import EvaluationRequest
from api.schemas import (
    EvaluationInput,
    EvaluationOutput,
    MetricResult,
)

app = FastAPI(
    title="AI Response Evaluation Framework API",
    version="2.2.0",
)

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


@app.get("/")
def home():
    return {
        "message": "AI Response Evaluation Framework API",
        "version": "2.2.0",
    }


@app.post(
    "/evaluate",
    response_model=EvaluationOutput,
)
def evaluate(data: EvaluationInput):

    report = engine.evaluate(
        EvaluationRequest(
            prompt=data.prompt,
            response=data.response,
        )
    )

    return EvaluationOutput(
        overall_score=report.overall_score,
        grade=report.grade,
        status=report.status,
        results=[
            MetricResult(
                metric_name=result.metric_name,
                score=result.score,
                feedback=result.feedback,
                passed=result.passed,
            )
            for result in report.results
        ],
    )
