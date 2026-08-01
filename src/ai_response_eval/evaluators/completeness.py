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

            # Coverage contributes 70% of the final score.
            keyword_score = coverage * 0.7

            if coverage == 0:
                length_score = 0.0
            else:
                length_ratio = min(
                    len(response_keywords) / (len(prompt_keywords) * 2),
                    1.0,
                )
                length_score = length_ratio * 0.3

            score = keyword_score + length_score

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
            return "The response thoroughly covers the requested topic."

        if score >= 0.70:
            return "The response covers most of the requested topic."

        if score >= 0.40:
            return "The response is only partially complete."

        return "The response is missing important information."
