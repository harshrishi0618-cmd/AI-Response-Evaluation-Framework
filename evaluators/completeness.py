from __future__ import annotations

from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult
from ai_response_eval.similarity.semantic import SemanticSimilarity
from ai_response_eval.utils.text import extract_keywords


class CompletenessEvaluator(BaseEvaluator):
    """
    Evaluates how completely the response answers the prompt.

    Scoring
    --------
    50% Semantic Coverage
    20% Keyword Coverage
    30% Information Density

    Completeness measures coverage, not factual correctness.
    """

    metric_name = "Completeness"

    def __init__(self) -> None:
        self.similarity = SemanticSimilarity()

    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:

        prompt = request.prompt.strip()
        response = request.response.strip()

        if not prompt or not response:
            return EvaluationResult(
                metric_name=self.metric_name,
                score=0.0,
                feedback="Prompt or response is empty.",
                passed=False,
            )

        # ----------------------------
        # Semantic Coverage
        # ----------------------------

        semantic_similarity = self.similarity.similarity(
            prompt,
            response,
        )

        semantic_score = semantic_similarity * 10

        # ----------------------------
        # Keyword Coverage
        # ----------------------------

        prompt_keywords = set(extract_keywords(prompt))
        response_keywords = set(extract_keywords(response))

        if prompt_keywords:
            keyword_score = (
                len(prompt_keywords & response_keywords) / len(prompt_keywords)
            ) * 10
        else:
            keyword_score = 10

        # ----------------------------
        # Information Density
        # ----------------------------

        word_count = len(response.split())

        if word_count >= 80:
            density_score = 10
        elif word_count >= 60:
            density_score = 9
        elif word_count >= 40:
            density_score = 8
        elif word_count >= 25:
            density_score = 7
        elif word_count >= 15:
            density_score = 5
        elif word_count >= 8:
            density_score = 3
        else:
            density_score = 1

        # Penalize extremely short answers
        if word_count <= 3:
            density_score = -2
        # ----------------------------
        # Final Score
        # ----------------------------

        final_score = (
            semantic_score * 0.40 + keyword_score * 0.20 + density_score * 0.40
        )

        final_score = round(max(0.0, min(10.0, final_score)), 1)

        if final_score >= 9:
            feedback = (
                "The response provides comprehensive coverage of the requested topic."
            )
        elif final_score >= 7:
            feedback = "The response covers most of the requested information."
        elif final_score >= 5:
            feedback = "The response answers the prompt but lacks important details."
        elif final_score >= 3:
            feedback = "The response only partially addresses the prompt."
        else:
            feedback = (
                "The response provides very little coverage of the requested topic."
            )

        return EvaluationResult(
            metric_name=self.metric_name,
            score=final_score,
            feedback=feedback,
            passed=final_score >= 7.0,
        )
