from __future__ import annotations

from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult
from ai_response_eval.utils.text import extract_keywords


class RelevanceEvaluator(BaseEvaluator):
    """
    Evaluates how relevant a response is to a given prompt.
    """

    @property
    def metric_name(self) -> str:
        return "Relevance"

    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:
        prompt_keywords = set(extract_keywords(request.prompt))
        response_keywords = set(extract_keywords(request.response))

        if not prompt_keywords:
            score = 0.0
        else:
            overlap = prompt_keywords & response_keywords
            score = (len(overlap) / len(prompt_keywords)) * 10

        feedback = self.generate_feedback(score)

        return EvaluationResult(
            metric=self.metric_name,
            score=round(score, 2),
            max_score=10,
            confidence=1.0,
            feedback=[feedback],
        )

    @staticmethod
    def _generate_feedback(score: float) -> str:
        if score >= 9:
            return "The response closely matches the prompt."

        if score >= 7:
            return "The response is mostly relevant."

        if score >= 4:
            return "The response is partially relevant."

        return "The response is largely unrelated to the prompt."
