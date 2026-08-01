from fastapi import APIRouter

from ai_response_eval.evaluation.engine import EvaluationEngine
from ai_response_eval.evaluators.clarity import ClarityEvaluator
from ai_response_eval.evaluators.completeness import CompletenessEvaluator
from ai_response_eval.evaluators.conciseness import ConcisenessEvaluator
from ai_response_eval.evaluators.relevance import RelevanceEvaluator
from ai_response_eval.evaluators.safety import SafetyEvaluator
from ai_response_eval.models.request import EvaluationRequest

from .schemas import EvaluationInput

router = APIRouter()


@router.get("/")
def root():
    return {"message": "AI Response Evaluation Framework API"}


@router.post("/evaluate")
def evaluate(data: EvaluationInput):

    engine = EvaluationEngine(
        evaluators=[
            RelevanceEvaluator(),
            CompletenessEvaluator(),
            ClarityEvaluator(),
            SafetyEvaluator(),
            ConcisenessEvaluator(),
        ]
    )

    report = engine.evaluate(
        EvaluationRequest(
            prompt=data.prompt,
            response=data.response,
        )
    )

    return {
        "overall_score": report.overall_score,
        "passed_metrics": report.passed_metrics,
        "failed_metrics": report.failed_metrics,
        "pass_rate": report.pass_rate,
        "results": [
            {
                "metric": r.metric_name,
                "score": r.score,
                "passed": r.passed,
                "feedback": r.feedback,
            }
            for r in report.results
        ],
    }
