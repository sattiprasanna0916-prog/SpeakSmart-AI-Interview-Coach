import librosa
import re
from collections import Counter


FILLER_WORDS = {
    "uh", "um", "ah", "like",
    "you know", "basically",
    "actually", "so"
}


def compute_audio_metrics(audio_path: str, transcript: str):
    """
    Computes:
    - duration
    - pause count
    - filler count
    - speech rate
    - fluency score

    Fluency scoring considers:
    - speaking pace
    - fillers
    - pauses
    - repetition
    - vocabulary variety
    - answer length
    """

    # --------------------------------
    # LOAD AUDIO
    # --------------------------------
    y, sr = librosa.load(
        audio_path,
        sr=16000,
        mono=True
    )

    duration = len(y) / sr if sr > 0 else 0

    # --------------------------------
    # PAUSE DETECTION
    # --------------------------------
    intervals = librosa.effects.split(
        y,
        top_db=35
    )

    pause_count = max(0, len(intervals) - 1)

    # avoid extreme values
    pause_count = min(pause_count, 20)

    # --------------------------------
    # TRANSCRIPT PROCESSING
    # --------------------------------
    words = re.findall(
        r"[a-zA-Z']+",
        (transcript or "").lower()
    )

    word_count = len(words)

    # --------------------------------
    # FILLER DETECTION
    # --------------------------------
    filler_count = sum(
        1 for w in words
        if w in FILLER_WORDS
    )

    # --------------------------------
    # SPEECH RATE
    # --------------------------------
    speech_rate = (
        (word_count / duration) * 60
        if duration > 0 else 0
    )

    # --------------------------------
    # VOCABULARY RICHNESS
    # --------------------------------
    unique_ratio = (
        len(set(words)) /
        max(1, word_count)
    )

    # --------------------------------
    # REPETITION CHECK
    # --------------------------------
    repeated_words = [
        word
        for word, count in Counter(words).items()
        if count >= 4
    ]

    # --------------------------------
    # FLUENCY SCORE
    # --------------------------------
    score = 6.5

    # --------------------
    # LENGTH
    # --------------------
    if word_count < 5:
        score -= 3
    elif word_count < 10:
        score -= 1.5
    elif word_count > 25:
        score += 0.5

    # --------------------
    # PAUSES
    # --------------------
    if pause_count > 12:
        score -= 2
    elif pause_count > 7:
        score -= 1
    elif pause_count <= 3 and word_count > 10:
        score += 0.5

    # --------------------
    # FILLERS
    # --------------------
    if filler_count >= 6:
        score -= 2
    elif filler_count >= 3:
        score -= 1
    elif filler_count == 0 and word_count > 10:
        score += 0.5

    # --------------------
    # SPEECH RATE
    # --------------------
    if speech_rate < 80:
        score -= 1.5
    elif speech_rate < 100:
        score -= 0.5
    elif 110 <= speech_rate <= 160:
        score += 1
    elif speech_rate > 190:
        score -= 1

    # --------------------
    # VOCABULARY
    # --------------------
    if unique_ratio < 0.45:
        score -= 2
    elif unique_ratio < 0.6:
        score -= 1
    elif unique_ratio > 0.8:
        score += 0.5

    # --------------------
    # REPETITION
    # --------------------
    if repeated_words:
        score -= 1

    # --------------------------------
    # FINAL CLAMP
    # --------------------------------
    score = max(
        0.0,
        min(10.0, round(score, 2))
    )

    return {
        "audio_duration": round(duration, 2),
        "pause_count": int(pause_count),
        "filler_count": int(filler_count),
        "speech_rate": round(speech_rate, 2),
        "fluency_score": score,
    }