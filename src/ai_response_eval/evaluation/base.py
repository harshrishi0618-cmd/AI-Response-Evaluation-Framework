from abc import ABC, abstractmethod

from ai_response_eval.models.request import EvaluationRequest
from ai_response_eval.models.result import EvaluationResult


class BaseEvaluator(ABC):
    """
    Abstract base class for all evaluators.

    Every evaluator must implement the evaluate() method.
    """

    @abstractmethod
    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        """
        Evaluate an AI response and return an EvaluationResult.
        """
        raise NotImplementedError
