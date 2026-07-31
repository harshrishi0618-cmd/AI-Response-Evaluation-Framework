from __future__ import annotations

import re

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
    # Question / instruction words
    "explain",
    "describe",
    "define",
    "tell",
    "show",
    "discuss",
    "list",
    "compare",
    "contrast",
    # Question words
    "what",
    "why",
    "how",
    "when",
    "where",
    "which",
    "who",
    # Request words
    "give",
    "provide",
    "write",
    "mention",
}


def normalize_text(text: str) -> str:
    """
    Convert text to lowercase and remove extra whitespace.
    """
    return " ".join(text.lower().split())


def tokenize(text: str) -> list[str]:
    """
    Split text into alphanumeric tokens.
    """
    return re.findall(r"\b\w+\b", text)


def remove_stopwords(tokens: list[str]) -> list[str]:
    """
    Remove common English stopwords.
    """
    return [token for token in tokens if token not in STOPWORDS]


def extract_keywords(text: str) -> list[str]:
    """
    Normalize text, tokenize it, and remove stopwords.
    """
    normalized = normalize_text(text)
    tokens = tokenize(normalized)
    return remove_stopwords(tokens)
