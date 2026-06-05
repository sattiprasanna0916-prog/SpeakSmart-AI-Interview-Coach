
from backend.db import get_connection
# --------------------------------
# REGISTER USER
# --------------------------------
def register_user(
    email,
    branch,
    current_level="Beginner"
):

    conn = get_connection()

    cur = conn.cursor()

    try:

        # CHECK EXISTING USER
        cur.execute(
            """
            SELECT user_id, email, branch, current_level
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        existing_user = cur.fetchone()

        if existing_user:

            return {
                "user_id": existing_user[0],
                "email": existing_user[1],
                "branch": existing_user[2],
                "current_level": existing_user[3]
            }

        # CREATE USER
        cur.execute(
            """
            INSERT INTO users (
                email,
                branch,
                current_level
            )
            VALUES (%s, %s, %s)
            RETURNING user_id
            """,
            (
                email,
                branch,
                current_level
            )
        )

        user_id = cur.fetchone()[0]

        conn.commit()

        # FETCH CREATED USER
        cur.execute(
            """
            SELECT user_id, email, branch, current_level
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        user = cur.fetchone()

        return {
            "user_id": user[0],
            "email": user[1],
            "branch": user[2],
            "current_level": user[3]
        }

    finally:

        conn.close()


# --------------------------------
# GET USER BY ID
# --------------------------------
def get_user(user_id):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT user_id, email, branch, current_level
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        user = cur.fetchone()

        if not user:
            return None

        return {
            "user_id": user[0],
            "email": user[1],
            "branch": user[2],
            "current_level": user[3]
        }

    finally:

        conn.close()


# --------------------------------
# GET USER BY EMAIL
# --------------------------------
def get_user_by_email(email):

    conn = get_connection()

    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT user_id, email, branch, current_level
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cur.fetchone()

        if not user:
            return None

        return {
            "user_id": user[0],
            "email": user[1],
            "branch": user[2],
            "current_level": user[3]
        }

    finally:

        conn.close()
