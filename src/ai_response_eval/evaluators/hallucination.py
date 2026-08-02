from __future__ import annotations

import re
from typing import ClassVar

from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.evaluators.scorer import ScoreBuilder
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult
from ai_response_eval.similarity.semantic import SemanticSimilarity


class HallucinationEvaluator(BaseEvaluator):
    """
    Estimates hallucination risk using semantic consistency
    and linguistic heuristics.

    NOTE:
    This evaluator estimates hallucination risk.
    It does NOT perform external fact verification.
    """

    metric_name = "Hallucination"

    FACTUAL_PATTERNS: ClassVar[list[str]] = [
        r"\binvented by\b",
        r"\bcreated by\b",
        r"\bfounded by\b",
        r"\bdiscovered by\b",
        r"\bpresident\b",
        r"\bprime minister\b",
        r"\bcapital of\b",
        r"\bceo\b",
        r"\baccording to\b",
        r"\bwon the\b",
        r"\bfirst\b",
        r"\bonly\b",
    ]

    HEDGING_PATTERNS: ClassVar[list[str]] = [
        r"\bmay\b",
        r"\bmight\b",
        r"\bpossibly\b",
        r"\bperhaps\b",
        r"\blikely\b",
        r"\bcould\b",
        r"\bappears\b",
        r"\bseems\b",
        r"\bapproximately\b",
    ]

    ABSOLUTE_PATTERNS: ClassVar[list[str]] = [
        r"\bdefinitely\b",
        r"\bguaranteed\b",
        r"\bproves\b",
        r"\bwithout doubt\b",
        r"\balways\b",
        r"\bnever\b",
        r"\b100%\b",
    ]

    YEAR_PATTERN = r"\b(?:18|19|20)\d{2}\b"

    def __init__(self) -> None:
        self.semantic = SemanticSimilarity()

    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:

        prompt = request.prompt.strip()
        response = request.response.strip()

        if not response:
            return EvaluationResult(
                metric_name=self.metric_name,
                score=0.0,
                feedback="Response is empty.",
                passed=False,
            )

        builder = ScoreBuilder()

        similarity = self.semantic.similarity(
            prompt,
            response,
        )

        # ----------------------------
        # Semantic mismatch
        # ----------------------------

        if similarity < 0.20:
            builder.penalize(True, 6)
        elif similarity < 0.40:
            builder.penalize(True, 4)
        elif similarity < 0.60:
            builder.penalize(True, 2)

        # ----------------------------
        # Factual claims
        # ----------------------------

        factual_claims = sum(
            bool(
                re.search(
                    pattern,
                    response,
                    re.IGNORECASE,
                )
            )
            for pattern in self.FACTUAL_PATTERNS
        )

        if factual_claims >= 2:
            builder.penalize(True, 5)
        elif factual_claims == 1:
            builder.penalize(True, 3)

        # ----------------------------
        # Absolute certainty
        # ----------------------------

        if any(
            re.search(pattern, response, re.IGNORECASE)
            for pattern in self.ABSOLUTE_PATTERNS
        ):
            builder.penalize(True, 4)

        # ----------------------------
        # Years increase factual risk
        # ----------------------------

        years = re.findall(
            self.YEAR_PATTERN,
            response,
        )

        if len(years) >= 1:
            builder.penalize(True, 2)

        # ----------------------------
        # Hedging lowers hallucination risk
        # ----------------------------

        if any(
            re.search(pattern, response, re.IGNORECASE)
            for pattern in self.HEDGING_PATTERNS
        ):
            builder.reward(True, 2)

        score = round(builder.clamp(), 1)

        if score >= 9:
            feedback = "Low hallucination risk detected."
        elif score >= 7:
            feedback = "Minor hallucination risk detected."
        elif score >= 5:
            feedback = "Moderate hallucination risk detected."
        else:
            feedback = "High hallucination risk detected."

        return EvaluationResult(
            metric_name=self.metric_name,
            score=score,
            feedback=feedback,
            passed=score >= 7,
        )
