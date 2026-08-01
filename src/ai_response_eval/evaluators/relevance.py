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
            score = len(overlap) / len(prompt_keywords)

        feedback = self._generate_feedback(score)

        return EvaluationResult(
            metric_name=self.metric_name,
            score=round(score, 2),
            feedback=feedback,
            passed=score >= 0.70,
        )

    @staticmethod
    def _generate_feedback(score: float) -> str:

        if score >= 0.90:
            return "The response closely matches the prompt."

        if score >= 0.70:
            return "The response is mostly relevant."

        if score >= 0.40:
            return "The response is partially relevant."

        return "The response is largely unrelated to the prompt."
