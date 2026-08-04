import re

from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult


class ClarityEvaluator(BaseEvaluator):
    """
    Evaluates how clear and readable an AI response is.
    """

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        response = request.response.strip()

        # Empty response
        if not response:
            return EvaluationResult(
                metric_name="Clarity",
                score=0.0,
                feedback="Response is empty.",
                passed=False,
            )

        score = 10.0

        # -----------------------------
        # 1. Sentence Length
        # -----------------------------
        sentences = [
            sentence.strip()
            for sentence in re.split(r"[.!?]+", response)
            if sentence.strip()
        ]

        if sentences:
            average_words = sum(len(sentence.split()) for sentence in sentences) / len(
                sentences
            )

            if average_words > 25:
                score -= 3

        # -----------------------------
        # 2. Repeated Words
        # -----------------------------
        words = [word.strip(".,!?").lower() for word in response.split()]

        if words:
            unique_ratio = len(set(words)) / len(words)

            if unique_ratio < 0.5:
                score -= 6

        # -----------------------------
        # 3. Filler Words
        # -----------------------------
        filler_words = {
            "actually",
            "basically",
            "really",
            "literally",
            "kind",
            "sort",
        }

        filler_count = sum(word in filler_words for word in words)

        if filler_count >= 3:
            score -= 3

        # Prevent negative scores
        score = max(score, 0.0)

        return EvaluationResult(
            metric_name="Clarity",
            score=round(score, 2),
            feedback="Clarity evaluated.",
            passed=score >= 7,
        )
