import re


def compute_grammar_score(transcript: str) -> float:
    """
    Computes grammar quality score (0–10)
    using lightweight NLP/rule-based checks.

    Focus areas:
    - sentence structure
    - capitalization
    - punctuation
    - repeated words
    - vocabulary richness
    - minimum meaningful response
    """

    if not transcript:
        return 0.0

    text = transcript.strip()

    if len(text) < 3:
        return 0.0

    score = 7.0  # strong baseline

    # --------------------------------
    # TOKENIZATION
    # --------------------------------
    words = re.findall(r"\b[a-zA-Z']+\b", text)
    word_count = len(words)

    if word_count == 0:
        return 0.0

    lower_words = [w.lower() for w in words]

    # --------------------------------
    # SHORT ANSWER PENALTY
    # --------------------------------
    if word_count < 5:
        score -= 3
    elif word_count < 10:
        score -= 1.5

    # --------------------------------
    # SENTENCE STRUCTURE
    # --------------------------------
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) == 0:
        score -= 2

    # --------------------------------
    # CAPITALIZATION CHECK
    # --------------------------------
    if text[0].islower():
        score -= 0.5

    # --------------------------------
    # PUNCTUATION CHECK
    # --------------------------------
    if text[-1] not in ".!?":
        score -= 0.5

    # --------------------------------
    # REPEATED WORDS
    # --------------------------------
    repeated_penalty = 0

    for i in range(1, len(lower_words)):
        if lower_words[i] == lower_words[i - 1]:
            repeated_penalty += 0.5

    score -= min(repeated_penalty, 2)

    # --------------------------------
    # VOCABULARY RICHNESS
    # --------------------------------
    unique_ratio = len(set(lower_words)) / word_count

    if unique_ratio < 0.45:
        score -= 2
    elif unique_ratio < 0.6:
        score -= 1
    elif unique_ratio > 0.8 and word_count > 12:
        score += 0.5

    # --------------------------------
    # BASIC CONNECTORS
    # --------------------------------
    connectors = {
        "because", "therefore", "however",
        "although", "moreover", "instead",
        "additionally", "while", "whereas"
    }

    if any(c in lower_words for c in connectors):
        score += 0.5

    # --------------------------------
    # CLAMP FINAL SCORE
    # --------------------------------
    score = max(0.0, min(10.0, round(score, 2)))

    return score