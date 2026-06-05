
import librosa
import re
from collections import Counter

FILLER_WORDS = {
    "uh", "um", "ah", "like",
    "basically", "actually", "so"
}

def compute_audio_metrics(audio_path: str, transcript: str):

    y, sr = librosa.load(
        audio_path,
        sr=16000,
        mono=True
    )

    duration = len(y) / sr if sr > 0 else 0

    intervals = librosa.effects.split(
        y,
        top_db=35
    )

    pause_count = max(0, len(intervals) - 1)
    pause_count = min(pause_count, 25)

    words = re.findall(
        r"[a-zA-Z']+",
        (transcript or "").lower()
    )

    word_count = len(words)

    filler_count = sum(
        1 for w in words
        if w in FILLER_WORDS
    )

    speech_rate = (
        (word_count / duration) * 60
        if duration > 0 else 0
    )

    unique_ratio = (
        len(set(words)) /
        max(1, word_count)
    )

    repeated_words = [
        word
        for word, count in Counter(words).items()
        if count >= 4
    ]

    score = 5.5

    # LENGTH
    if word_count < 5:
        score = min(score, 2)

    elif word_count < 10:
        score = min(score, 4)

    elif word_count < 20:
        score = min(score, 6)

    elif word_count > 40:
        score += 0.5

    # PAUSES
    if pause_count > 15:
        score -= 2.5

    elif pause_count > 10:
        score -= 1.5

    elif pause_count > 6:
        score -= 0.8

    elif pause_count <= 2 and word_count > 15:
        score += 0.5

    # FILLERS
    if filler_count >= 6:
        score -= 2.5

    elif filler_count >= 4:
        score -= 1.5

    elif filler_count >= 2:
        score -= 0.5

    elif filler_count == 0 and word_count > 15:
        score += 0.5

    # SPEECH RATE
    if speech_rate < 70:
        score -= 2

    elif speech_rate < 100:
        score -= 1

    elif 110 <= speech_rate <= 155:
        score += 1

    elif 155 < speech_rate <= 180:
        score += 0.3

    elif speech_rate > 190:
        score -= 1.5

    # VOCABULARY
    if unique_ratio < 0.45:
        score -= 2

    elif unique_ratio < 0.6:
        score -= 1

    elif unique_ratio > 0.8:
        score += 0.5

    # REPETITION
    if repeated_words:
        score -= 1.5

    score = max(
        0.0,
        min(10.0, round(score, 2))
    )

    if score < 4:
        label = "Needs Improvement"

    elif score < 7:
        label = "Average"

    elif score < 8.5:
        label = "Good"

    else:
        label = "Excellent"

    return {
        "audio_duration": round(duration, 2),
        "pause_count": int(pause_count),
        "filler_count": int(filler_count),
        "speech_rate": round(speech_rate, 2),
        "fluency_score": score,
        "fluency_label": label,
    }
