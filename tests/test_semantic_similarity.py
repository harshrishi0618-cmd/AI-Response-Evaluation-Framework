from ai_response_eval.similarity.semantic import SemanticSimilarity


def test_similarity_identical_text():
    model = SemanticSimilarity()

    score = model.similarity(
        "Python is great",
        "Python is great",
    )

    assert score > 0.99


def test_similarity_related_text():
    model = SemanticSimilarity()

    score = model.similarity(
        "Artificial Intelligence",
        "AI",
    )

    assert score > 0.4


def test_similarity_unrelated_text():
    model = SemanticSimilarity()

    score = model.similarity(
        "Python programming",
        "Chocolate cake",
    )

    assert score < 0.5
