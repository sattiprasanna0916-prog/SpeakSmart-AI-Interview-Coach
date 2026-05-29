from backend.db import get_connection

from backend.services.progress_service import (
    compute_progress,
    get_current_level
)


LEVEL_ORDER = [
    "Beginner",
    "Intermediate",
    "Advanced"
]


# --------------------------------
# GET NEXT LEVEL
# --------------------------------
def get_next_level(level: str) -> str:

    try:
        index = LEVEL_ORDER.index(level)

        return LEVEL_ORDER[
            min(index + 1, len(LEVEL_ORDER) - 1)
        ]

    except Exception:
        return "Beginner"


# --------------------------------
# EVALUATE USER LEVEL
# --------------------------------
def evaluate_and_update_level(user_id: int):

    progress = compute_progress(user_id)

    current_level = str(
        progress.get(
            "current_level",
            get_current_level(user_id)
        )
    ).strip().title()

    total_attempts = progress.get(
        "total_attempts",
        0
    )

    # --------------------------------
    # NO ATTEMPTS
    # --------------------------------
    if total_attempts == 0:

        return {
            "message": "No attempts available",
            "current_level": current_level,
            "suggested_level": current_level,
            "total_attempts": 0,
            "avg_score": 0,
        }

    # --------------------------------
    # SCORES
    # --------------------------------
    avg_fluency = progress.get(
        "avg_fluency",
        0
    )

    avg_grammar = progress.get(
        "avg_grammar",
        0
    )

    avg_accuracy = progress.get(
        "avg_accuracy",
        0
    )

    valid_scores = [
        score for score in [
            avg_fluency,
            avg_grammar,
            avg_accuracy
        ]
        if score > 0
    ]

    avg_score = (
        sum(valid_scores) /
        len(valid_scores)
        if valid_scores else 0
    )

    # --------------------------------
    # REQUIREMENTS
    # --------------------------------
    REQUIRED_ATTEMPTS = 5
    REQUIRED_SCORE = 8

    if total_attempts < REQUIRED_ATTEMPTS:

        remaining = (
            REQUIRED_ATTEMPTS -
            total_attempts
        )

        return {
            "message": (
                f"Complete {remaining} more "
                f"attempt(s) to level up."
            ),
            "current_level": current_level,
            "suggested_level": current_level,
            "total_attempts": total_attempts,
            "avg_score": round(avg_score, 2),
        }

    if avg_score < REQUIRED_SCORE:

        return {
            "message": (
                "Average score must be "
                "8 or higher to level up."
            ),
            "current_level": current_level,
            "suggested_level": current_level,
            "total_attempts": total_attempts,
            "avg_score": round(avg_score, 2),
        }

    # --------------------------------
    # MAX LEVEL
    # --------------------------------
    if current_level == "Advanced":

        return {
            "message": (
                "You are already at "
                "the highest level."
            ),
            "current_level": current_level,
            "suggested_level": current_level,
            "total_attempts": total_attempts,
            "avg_score": round(avg_score, 2),
        }

    # --------------------------------
    # UPDATE LEVEL
    # --------------------------------
    new_level = get_next_level(current_level)

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            UPDATE users
            SET current_level = ?
            WHERE user_id = ?
            """,
            (
                new_level,
                user_id
            )
        )

        conn.commit()

    finally:
        conn.close()

    return {
        "message": (
            f"Level Up! "
            f"{current_level} → {new_level}"
        ),
        "current_level": new_level,
        "suggested_level": new_level,
        "total_attempts": total_attempts,
        "avg_score": round(avg_score, 2),
    }