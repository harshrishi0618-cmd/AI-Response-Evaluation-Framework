from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from ai_response_eval.similarity.base import SimilarityModel


class SemanticSimilarity(SimilarityModel):
    """
    Computes semantic similarity using Sentence Transformers.
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def similarity(self, text1: str, text2: str) -> float:
        embeddings = self.model.encode(
            [text1, text2],
            convert_to_tensor=True,
        )

        score = cos_sim(
            embeddings[0],
            embeddings[1],
        ).item()

        return round(float(score), 4)
