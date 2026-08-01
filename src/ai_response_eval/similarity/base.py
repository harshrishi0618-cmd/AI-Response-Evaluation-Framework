from abc import ABC, abstractmethod


class SimilarityModel(ABC):
    """
    Base class for similarity models.
    """

    @abstractmethod
    def similarity(self, text1: str, text2: str) -> float:
        """
        Return a similarity score between 0 and 1.
        """
        raise NotImplementedError
