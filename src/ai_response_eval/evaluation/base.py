from __future__ import annotations

from abc import ABC, abstractmethod

from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult


class BaseEvaluator(ABC):
    """
    Base class for all evaluation metrics.
    """

    @property
    @abstractmethod
    def metric_name(self) -> str:
        raise NotImplementedError

    @property
    def max_score(self) -> float:
        return 10.0

    @abstractmethod
    def evaluate(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResult:
        raise NotImplementedError

    def generate_feedback(self, score: float) -> str:
        """
        Generate generic feedback based on score.
        """

        if score >= 9:
            return "Excellent."

        if score >= 7:
            return "Good."

        if score >= 4:
            return "Needs improvement."

        return "Poor."
