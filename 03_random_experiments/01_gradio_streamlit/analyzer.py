"""Shared text-analysis logic.

Both the Gradio and Streamlit apps import this function. Keeping the actual
"work" here means the two app files differ ONLY in their UI code, so you can
compare the two libraries directly without the analysis logic getting in the way.
"""

import re


def analyze_text(text: str) -> dict:
    """Return basic statistics about a piece of text.

    Args:
        text: the raw text to analyze.

    Returns:
        A dict with word/character/sentence counts and the longest word.
    """
    text = (text or "").strip()

    # Characters including spaces, and excluding spaces.
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))

    # Words: split on any run of whitespace. Filter out empties.
    words = [w for w in re.split(r"\s+", text) if w]
    word_count = len(words)

    # Sentences: split on . ! ? and count the non-empty pieces.
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    sentence_count = len(sentences)

    # Longest word (strip surrounding punctuation so "hello!" counts as "hello").
    cleaned = [re.sub(r"[^\w]", "", w) for w in words]
    longest_word = max(cleaned, key=len) if cleaned else ""

    return {
        "word_count": word_count,
        "char_count": char_count,
        "char_count_no_spaces": char_count_no_spaces,
        "sentence_count": sentence_count,
        "longest_word": longest_word,
    }
