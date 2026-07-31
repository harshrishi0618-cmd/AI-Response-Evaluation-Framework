from ai_response_eval.utils.text import (
    extract_keywords,
    normalize_text,
    remove_stopwords,
    tokenize,
)


def test_normalize_text():
    text = "  Machine   Learning IS   Awesome  "

    assert normalize_text(text) == "machine learning is awesome"


def test_tokenize():
    text = "machine learning, is awesome!"

    assert tokenize(text) == [
        "machine",
        "learning",
        "is",
        "awesome",
    ]


def test_remove_stopwords():
    tokens = [
        "machine",
        "learning",
        "is",
        "awesome",
    ]

    assert remove_stopwords(tokens) == [
        "machine",
        "learning",
        "awesome",
    ]


def test_extract_keywords():
    text = "The Machine Learning model is amazing!"

    assert extract_keywords(text) == [
        "machine",
        "learning",
        "model",
        "amazing",
    ]
