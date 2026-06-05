from backend.db import get_connection


# --------------------------------
# SAVE INTERVIEW ATTEMPT
# --------------------------------
def save_attempt(**data):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO attempts (
                user_id,
                level,
                question,
                answer_text,
                audio_duration,
                pause_count,
                filler_count,
                speech_rate,
                fluency_score,
                grammar_score,
                accuracy_score,
                final_score,
                feedback,
                improved_answer
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data["user_id"],
                data["level"],
                data["question"],
                data["answer_text"],
                data["audio_duration"],
                data["pause_count"],
                data["filler_count"],
                data["speech_rate"],
                data["fluency_score"],
                data["grammar_score"],
                data["accuracy_score"],
                data["final_score"],
                data["feedback"],
                data["improved_answer"],
            )
        )

        conn.commit()

        return {
            "status": "success"
        }

    finally:
        conn.close()


# --------------------------------
# GET USER ATTEMPTS
# --------------------------------
def get_user_attempts(user_id):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT *
            FROM attempts
            WHERE user_id = %s
            ORDER BY created_at DESC
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