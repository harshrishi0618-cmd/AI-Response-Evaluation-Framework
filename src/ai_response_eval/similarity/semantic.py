from __future__ import annotations

from threading import Lock
from typing import ClassVar

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from ai_response_eval.similarity.base import SimilarityModel


class SemanticSimilarity(SimilarityModel):
    """
    Computes semantic similarity using Sentence Transformers.

    Features
    --------
    - Singleton model (loaded only once)
    - Thread-safe lazy initialization
    - Embedding cache
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    _model: SentenceTransformer | None = None
    _lock = Lock()
    _embedding_cache: ClassVar[dict[str, object]] = {}

    def __init__(self) -> None:
        if SemanticSimilarity._model is None:
            with SemanticSimilarity._lock:
                if SemanticSimilarity._model is None:
                    print(f"Loading SentenceTransformer: {self.MODEL_NAME}")
                    SemanticSimilarity._model = SentenceTransformer(self.MODEL_NAME)

        self.model = SemanticSimilarity._model

    def _encode(self, text: str):
        """
        Returns cached embedding if available.
        """

        cached = SemanticSimilarity._embedding_cache.get(text)

        if cached is not None:
            return cached

        embedding = self.model.encode(
            text,
            convert_to_tensor=True,
        )

        SemanticSimilarity._embedding_cache[text] = embedding

        return embedding

    def similarity(
        self,
        text1: str,
        text2: str,
    ) -> float:

        embedding1 = self._encode(text1)
        embedding2 = self._encode(text2)

        score = cos_sim(
            embedding1,
            embedding2,
        ).item()

        return round(float(score), 4)

    @classmethod
    def clear_cache(cls) -> None:
        """
        Clears cached embeddings.
        Useful for tests or long-running services.
        """
        cls._embedding_cache.clear()
