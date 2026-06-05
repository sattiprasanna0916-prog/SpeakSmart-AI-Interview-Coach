from datetime import datetime, timedelta

from backend.db import get_connection


# --------------------------------
# NORMALIZE LEVEL
# --------------------------------
def normalize_level(level: str) -> str:

    value = str(level or "").strip().lower()

    mapping = {
        "1": "Beginner",
        "2": "Intermediate",
        "3": "Advanced",
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
    }

    return mapping.get(value, "Beginner")


# --------------------------------
# GET CURRENT LEVEL
# --------------------------------
def get_current_level(user_id: int) -> str:

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT current_level
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        row = cur.fetchone()

        if not row:
            return "Beginner"

        return normalize_level(
            row[0]
        )

    finally:
        conn.close()


# --------------------------------
# LOAD USER ATTEMPTS
# --------------------------------
def load_attempts(user_id: int):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT *
            FROM attempts
            WHERE user_id = %s
            ORDER BY created_at
            """,
            (user_id,)
        )

        rows = cur.fetchall()

        return [
    {
        "id": r[0],
        "user_id": r[1],
        "level": r[2],
        "question": r[3],
        "answer_text": r[4],
        "audio_duration": r[5],
        "pause_count": r[6],
        "filler_count": r[7],
        "speech_rate": r[8],
        "fluency_score": r[9],
        "grammar_score": r[10],
        "accuracy_score": r[11],
        "final_score": r[12],
        "feedback": r[13],
        "improved_answer": r[14],
        "created_at": str(r[15])
    }
    for r in rows
]

    finally:
        conn.close()


# --------------------------------
# CALCULATE STREAK
# --------------------------------
def calculate_streak(rows):

    if not rows:
        return 0

    try:
        dates = [
            datetime.fromisoformat(
                row["created_at"]
            ).date()
            for row in rows
            if row.get("created_at")
        ]

        unique_dates = sorted(set(dates))

        if not unique_dates:
            return 0

        today = datetime.now().date()

        streak = 0
        current_day = today

        for day in reversed(unique_dates):

            if day == current_day:
                streak += 1
                current_day -= timedelta(days=1)

            elif day < current_day:
                break

        return streak

    except Exception:
        return 0


# --------------------------------
# COMPUTE USER PROGRESS
# --------------------------------
def compute_progress(user_id: int):

    current_level = get_current_level(user_id)

    rows = load_attempts(user_id)

    if not rows:
        return {
            "current_level": current_level,
            "total_attempts": 0,
            "avg_fluency": 0,
            "avg_grammar": 0,
            "avg_accuracy": 0,
            "avg_final": 0,
            "weakest_skill": "-",
            "streak_days": 0,
            "history_labels": [],
            "history_scores": [],
        }

    # --------------------------------
    # SCORES
    # --------------------------------
    fluency_scores = [
        row.get("fluency_score", 0) or 0
        for row in rows
    ]

    grammar_scores = [
        row.get("grammar_score", 0) or 0
        for row in rows
    ]

    accuracy_scores = [
        row.get("accuracy_score", 0) or 0
        for row in rows
    ]

    avg_fluency = (
        sum(fluency_scores) /
        len(fluency_scores)
    )

    avg_grammar = (
        sum(grammar_scores) /
        len(grammar_scores)
    )

    avg_accuracy = (
        sum(accuracy_scores) /
        len(accuracy_scores)
    )

    avg_final = (
        avg_fluency +
        avg_grammar +
        avg_accuracy
    ) / 3

    # --------------------------------
    # WEAKEST SKILL
    # --------------------------------
    skills = {
        "Fluency": avg_fluency,
        "Grammar": avg_grammar,
        "Accuracy": avg_accuracy,
    }

    weakest_skill = min(
        skills,
        key=skills.get
    )

    # --------------------------------
    # STREAK
    # --------------------------------
    streak_days = calculate_streak(rows)

    # --------------------------------
    # CHART DATA
    # --------------------------------
    recent_rows = rows[-10:]

    history_labels = [
        row["created_at"][5:10]
        if row.get("created_at")
        else ""
        for row in recent_rows
    ]

    history_scores = [
        round(
            (
                row.get("fluency_score", 0) +
                row.get("grammar_score", 0) +
                row.get("accuracy_score", 0)
            ) / 3,
            2
        )
        for row in recent_rows
    ]

    return {
        "current_level": current_level,

        "total_attempts": len(rows),

        "avg_fluency": round(avg_fluency, 2),
        "avg_grammar": round(avg_grammar, 2),
        "avg_accuracy": round(avg_accuracy, 2),
        "avg_final": round(avg_final, 2),

        "weakest_skill": weakest_skill,

        "streak_days": streak_days,

        "history_labels": history_labels,
        "history_scores": history_scores,
    }