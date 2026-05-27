import re
from collections import Counter


STOPWORDS = {
    "the", "is", "are", "a", "an", "to", "of",
    "and", "in", "on", "for", "with", "that",
    "this", "it", "as", "was", "were", "be",
    "have", "has", "had", "at", "by", "from"
}


def extract_keywords(text: str):
    words = re.findall(r"\b[a-zA-Z']+\b", text.lower())

    keywords = [
        w for w in words
        if w not in STOPWORDS and len(w) > 2
    ]

    return keywords


def compute_accuracy_details(transcript: str, question: str) -> dict:
    """
    Evaluates how relevant the user's answer is
    to the interview question.

    Factors:
    - keyword relevance
    - semantic coverage
    - answer completeness
    - vocabulary quality
    - response length
    """

    transcript = (transcript or "").strip()
    question = (question or "").strip()

    if not transcript or not question:
        return {
            "score": 0.0,
            "matched_keywords": [],
            "missing_keywords": [],
            "keyword_coverage": 0.0,
            "relevance_ratio": 0.0,
        }

    # --------------------------------
    # KEYWORD EXTRACTION
    # --------------------------------
    answer_keywords = extract_keywords(transcript)
    question_keywords = extract_keywords(question)

    answer_set = set(answer_keywords)
    question_set = set(question_keywords)

    # --------------------------------
    # MATCHING
    # --------------------------------
    matched = sorted(list(answer_set & question_set))
    missing = sorted(list(question_set - answer_set))

    coverage = (
        len(matched) / max(1, len(question_set))
    )

    # --------------------------------
    # WORD QUALITY
    # --------------------------------
    word_count = len(answer_keywords)

    unique_ratio = (
        len(set(answer_keywords)) /
        max(1, word_count)
    )

    # --------------------------------
    # RELEVANCE RATIO
    # --------------------------------
    relevant_words = sum(
        1 for w in answer_keywords
        if w in question_set
    )

    relevance_ratio = (
        relevant_words / max(1, word_count)
    )

    # --------------------------------
    # BASE SCORE
    # --------------------------------
    score = 0

    # keyword coverage
    score += coverage * 5

    # relevance
    score += relevance_ratio * 3

    # vocabulary richness
    if unique_ratio > 0.7:
        score += 1

    # sufficient explanation
    if word_count > 15:
        score += 1

    # --------------------------------
    # PENALTIES
    # --------------------------------
    if word_count < 5:
        score -= 3
    elif word_count < 10:
        score -= 1.5

    # repetitive response
    repeated_words = [
        word
        for word, count in Counter(answer_keywords).items()
        if count >= 4
    ]

    if repeated_words:
        score -= 1

    # --------------------------------
    # CLAMP
    # --------------------------------
    score = max(0.0, min(10.0, round(score, 2)))

    return {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "keyword_coverage": round(coverage, 3),
        "relevance_ratio": round(relevance_ratio, 3),
    }


def compute_accuracy_score(transcript: str, question: str) -> float:
    return float(
        compute_accuracy_details(
            transcript,
            question
        )["score"]
    )