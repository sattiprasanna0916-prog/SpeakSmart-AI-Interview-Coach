
import re
from collections import Counter
# --------------------------------
# STOPWORDS
# --------------------------------
STOPWORDS = {
    "the", "is", "are", "a", "an", "to",
    "of", "and", "in", "on", "for",
    "with", "that", "this", "it",
    "as", "was", "were", "be",
    "have", "has", "had", "at",
    "by", "from"
}
# --------------------------------
# GENERIC PHRASES
# --------------------------------
GENERIC_TERMS = {
    "hardworking",
    "passionate",
    "quick learner",
    "team player",
    "dedicated",
    "motivated",
    "good communication",
    "leadership"
}
# --------------------------------
# KEYWORD EXTRACTION
# --------------------------------
def extract_keywords(text: str):
    words = re.findall(
        r"\b[a-zA-Z']+\b",
        text.lower()
    )
    keywords = [
        w for w in words
        if w not in STOPWORDS
        and len(w) > 2
    ]
    return keywords
# --------------------------------
# MAIN ACCURACY EVALUATION
# --------------------------------
def compute_accuracy_details(
    transcript: str,
    question: str
) -> dict:
    transcript = (
        transcript or ""
    ).strip()
    question = (
        question or ""
    ).strip()
    # EMPTY CHECK
    if not transcript or not question:
        return {
            "score": 0.0,
            "label": "Needs Improvement",
            "matched_keywords": [],
            "missing_keywords": [],
            "keyword_coverage": 0.0,
            "relevance_ratio": 0.0,
        }
    # --------------------------------
    # EXTRACT KEYWORDS
    # --------------------------------
    answer_keywords = extract_keywords(
        transcript
    )
    question_keywords = extract_keywords(
        question
    )
    answer_set = set(answer_keywords)
    question_set = set(question_keywords)
    # --------------------------------
    # KEYWORD MATCHING
    # --------------------------------
    matched = sorted(
        list(answer_set & question_set)
    )
    missing = sorted(
        list(question_set - answer_set)
    )
    coverage = (
        len(matched)
        / max(1, len(question_set))
    )
    # --------------------------------
    # RESPONSE STATS
    # --------------------------------
    word_count = len(answer_keywords)
    unique_ratio = (
        len(set(answer_keywords))
        / max(1, word_count)
    )
    relevant_words = sum(
        1 for w in answer_keywords
        if w in question_set
    )
    relevance_ratio = (
        relevant_words
        / max(1, word_count)
    )
    # --------------------------------
    # BASE SCORE
    # --------------------------------
    score = 0
    # KEYWORD COVERAGE
    score += coverage * 4
    # RELEVANCE
    score += relevance_ratio * 2.5
    # VOCABULARY QUALITY
    if unique_ratio > 0.75:
        score += 1
    # GOOD LENGTH BONUS
    if word_count > 35:
        score += 1.5
    elif word_count > 20:
        score += 1
    # --------------------------------
    # STRICT LENGTH PENALTIES
    # --------------------------------
    if word_count < 5:
        score = min(score, 2)
    elif word_count < 10:
        score = min(score, 4)
    elif word_count < 20:
        score = min(score, 6)
    # --------------------------------
    # REPETITION PENALTY
    # --------------------------------
    repeated_words = [
        word
        for word, count
        in Counter(answer_keywords).items()
        if count >= 4
    ]
    if repeated_words:
        score -= 1.5
    # --------------------------------
    # GENERIC ANSWER PENALTY
    # --------------------------------
    generic_hits = sum(
        1 for phrase in GENERIC_TERMS
        if phrase in transcript.lower()
    )
    if generic_hits >= 2:
        score -= 1.5
    elif generic_hits == 1:
        score -= 0.5
    # --------------------------------
    # LOW RELEVANCE PENALTY
    # --------------------------------
    if relevance_ratio < 0.15:
        score -= 2
    # --------------------------------
    # FINAL CLAMP
    # --------------------------------
    score = max(
        0.0,
        min(10.0, round(score, 2))
    )
    # --------------------------------
    # LABELS
    # --------------------------------
    if score < 4:
        label = "Needs Improvement"
    elif score < 7:
        label = "Average"
    elif score < 8.5:
        label = "Good"
    else:
        label = "Excellent"
    # --------------------------------
    # RETURN
    # --------------------------------
    return {
        "score": score,
        "label": label,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "keyword_coverage": round(
            coverage, 3
        ),
        "relevance_ratio": round(
            relevance_ratio, 3
        ),
    }
# --------------------------------
# SIMPLE SCORE HELPER
# --------------------------------
def compute_accuracy_score(
    transcript: str,
    question: str
) -> float:
    return float(
        compute_accuracy_details(
            transcript,
            question
        )["score"]
    )
