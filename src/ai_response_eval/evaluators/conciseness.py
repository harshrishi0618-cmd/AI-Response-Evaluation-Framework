import re
from collections import Counter
from typing import ClassVar

from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.evaluators.scorer import ScoreBuilder
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult


class ConcisenessEvaluator(BaseEvaluator):
    """
    Evaluates how concise an AI response is.
    """

    FILLER_WORDS: ClassVar[set[str]] = {
        "basically",
        "actually",
        "really",
        "very",
        "kind",
        "extremely",
        "literally",
        "quite",
    }

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        response = request.response.strip()

        if not response:
            return EvaluationResult(
                metric_name="Conciseness",
                score=0.0,
                feedback="Response is empty.",
                passed=False,
            )

        builder = ScoreBuilder()

        words = re.findall(r"\b[\w-]+\b", response.lower())

        builder.penalize(
            self._has_repeated_words(words),
            3,
        )

        builder.penalize(
            self._has_repeated_sentences(response),
            3,
        )

        builder.penalize(
            self._has_filler_words(words),
            3,
        )

        builder.penalize(
            self._is_too_verbose(words),
            1,
        )

        builder.penalize(
            self._low_lexical_diversity(words),
            2,
        )

        score = builder.clamp()

        if score >= 8:
            feedback = "Response is concise."
        elif score >= 5:
            feedback = "Response could be more concise."
        else:
            feedback = "Response is overly repetitive or verbose."

        return EvaluationResult(
            metric_name="Conciseness",
            score=score,
            feedback=feedback,
            passed=score >= 7,
        )

    def _has_repeated_words(self, words: list[str]) -> bool:
        counts = Counter(words)
        return any(count >= 3 for count in counts.values())

    def _has_repeated_sentences(self, response: str) -> bool:
        sentences = [
            sentence.strip().lower()
            for sentence in re.split(r"[.!?]+", response)
            if sentence.strip()
        ]

        counts = Counter(sentences)

        return any(count >= 2 for count in counts.values())

    def _has_filler_words(self, words: list[str]) -> bool:
        filler_count = sum(word in self.FILLER_WORDS for word in words)
        return filler_count >= 2

    def _is_too_verbose(self, words: list[str]) -> bool:
        return len(words) > 60

    def _low_lexical_diversity(self, words: list[str]) -> bool:
        if len(words) < 5:
            return False

        diversity = len(set(words)) / len(words)
        return diversity < 0.5
