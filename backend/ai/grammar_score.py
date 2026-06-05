
import re
# --------------------------------
# MAIN GRAMMAR SCORING
# --------------------------------
def compute_grammar_details(
    transcript: str
) -> dict:
    if not transcript:
        return {
            "score": 0.0,
            "label": "Needs Improvement"
        }
    text = transcript.strip()
    if len(text) < 3:
        return {
            "score": 0.0,
            "label": "Needs Improvement"
        }
    # --------------------------------
    # LOWER BASELINE
    # --------------------------------
    score = 5.5
    # --------------------------------
    # TOKENIZATION
    # --------------------------------
    words = re.findall(
        r"\b[a-zA-Z']+\b",
        text
    )
    word_count = len(words)
    if word_count == 0:
        return {
            "score": 0.0,
            "label": "Needs Improvement"
        }
    lower_words = [
        w.lower()
        for w in words
    ]
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
    # SENTENCE STRUCTURE
    # --------------------------------
    sentences = re.split(
        r"[.!?]+",
        text
    )
    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]
    if len(sentences) == 0:
        score -= 2
    # --------------------------------
    # CAPITALIZATION
    # --------------------------------
    if text[0].islower():
        score -= 0.5
    # --------------------------------
    # PUNCTUATION
    # --------------------------------
    if text[-1] not in ".!?":
        score -= 0.5
    # --------------------------------
    # REPEATED WORDS
    # --------------------------------
    repeated_penalty = 0
    for i in range(
        1,
        len(lower_words)
    ):
        if lower_words[i] == lower_words[i - 1]:
            repeated_penalty += 0.5
    score -= min(
        repeated_penalty,
        2
    )
    # --------------------------------
    # VOCABULARY RICHNESS
    # --------------------------------
    unique_ratio = (
        len(set(lower_words))
        / word_count
    )
    if unique_ratio < 0.45:
        score -= 2
    elif unique_ratio < 0.6:
        score -= 1
    elif (
        unique_ratio > 0.8
        and word_count > 12
    ):
        score += 0.5
    # --------------------------------
    # CONNECTOR WORD BONUS
    # --------------------------------
    connectors = {
        "because",
        "therefore",
        "however",
        "although",
        "moreover",
        "instead",
        "additionally",
        "while",
        "whereas"
    }
    if any(
        c in lower_words
        for c in connectors
    ):
        score += 0.3
    # --------------------------------
    # FILLER WORD PENALTY
    # --------------------------------
    fillers = {
        "um",
        "uh",
        "like",
        "actually",
        "basically"
    }
    filler_count = sum(
        1 for word in lower_words
        if word in fillers
    )
    if filler_count >= 5:
        score -= 2
    elif filler_count >= 3:
        score -= 1
    # --------------------------------
    # RUN-ON SENTENCE PENALTY
    # --------------------------------
    for sentence in sentences:
        sentence_words = sentence.split()
        if len(sentence_words) > 35:
            score -= 1
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

        "label": label
    }
# --------------------------------
# SIMPLE SCORE FUNCTION
# --------------------------------
def compute_grammar_score(
    transcript: str
) -> float:
    return float(
        compute_grammar_details(
            transcript
        )["score"]
    )

