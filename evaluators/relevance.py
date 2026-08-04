from __future__ import annotations

import re
from typing import ClassVar

from ai_response_eval.evaluation.base import BaseEvaluator
from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult
from ai_response_eval.similarity.semantic import SemanticSimilarity


class RelevanceEvaluator(BaseEvaluator):
    """
    Evaluates how relevant the response is to the user's prompt.

    Score Components
    ----------------
    80% Semantic Similarity
    20% Prompt Concept Coverage

    NOTE:
    Relevance measures topical alignment ONLY.
    It intentionally does NOT judge factual correctness.
    Incorrect facts should be handled by HallucinationEvaluator.
    """

    metric_name = "Relevance"

    STOPWORDS: ClassVar[set[str]] = {
        "what",
        "who",
        "where",
        "when",
        "why",
        "how",
        "is",
        "are",
        "was",
        "were",
        "the",
        "a",
        "an",
        "of",
        "to",
        "for",
        "in",
        "on",
        "and",
        "or",
        "about",
        "explain",
        "describe",
        "tell",
        "me",
        "define",
        "give",
    }

    def __init__(self) -> None:
        self.similarity = SemanticSimilarity()

    def _extract_keywords(self, text: str) -> set[str]:
        words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9]+\b", text.lower())

        return {word for word in words if word not in self.STOPWORDS and len(word) > 2}

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
                passed=False,
                feedback="Prompt or response is empty.",
            )

        semantic_similarity = self.similarity.similarity(
            prompt,
            response,
        )

        prompt_keywords = self._extract_keywords(prompt)
        response_words = set(
            re.findall(
                r"\b[a-zA-Z][a-zA-Z0-9]+\b",
                response.lower(),
            )
        )

        if prompt_keywords:
            coverage = len(prompt_keywords & response_words) / len(prompt_keywords)
        else:
            coverage = 1.0

        semantic_score = semantic_similarity * 10
        keyword_score = coverage * 10

        final_score = semantic_score * 0.80 + keyword_score * 0.20

        final_score = round(
            max(
                0.0,
                min(10.0, final_score),
            ),
            1,
        )

        if final_score >= 9:
            feedback = "The response is highly relevant to the prompt."

        elif final_score >= 7:
            feedback = "The response is relevant and addresses the prompt."

        elif final_score >= 5:
            feedback = "The response is somewhat relevant but lacks focus."

        elif final_score >= 3:
            feedback = "The response is only loosely related to the prompt."

        else:
            feedback = "The response is not relevant to the prompt."

        return EvaluationResult(
            metric_name=self.metric_name,
            score=final_score,
            passed=final_score >= 6.0,
            feedback=feedback,
        )
