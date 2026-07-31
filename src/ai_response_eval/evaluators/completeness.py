from __future__ import annotations

from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult
from ai_response_eval.utils.text import extract_keywords


class CompletenessEvaluator(BaseEvaluator):
    """
    Evaluates whether the response sufficiently covers
    the concepts requested in the prompt.
    """

    @property
    def metric_name(self) -> str:
        return "Completeness"

    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:

        prompt_keywords = set(extract_keywords(request.prompt))
        response_keywords = set(extract_keywords(request.response))

        if not prompt_keywords:
            score = 0.0

        else:
            overlap = len(prompt_keywords & response_keywords)
            coverage = overlap / len(prompt_keywords)

            bonus = 0

            if len(response_keywords) >= len(prompt_keywords) * 2:
                bonus = 2

            score = min((coverage * 8) + bonus, 10)

        feedback = self._generate_feedback(score)

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
            return "The response thoroughly covers the requested topic."

        if score >= 7:
            return "The response covers most of the requested topic."

        if score >= 4:
            return "The response is only partially complete."

        return "The response is missing important information."
