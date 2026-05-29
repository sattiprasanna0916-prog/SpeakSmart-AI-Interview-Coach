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
        # ----------------------------
        # CHECK EXISTING USER
        # ----------------------------
        cur.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        existing_user = cur.fetchone()

        if existing_user:
            return dict(existing_user)

        # ----------------------------
        # CREATE USER
        # ----------------------------
        cur.execute(
            """
            INSERT INTO users (
                email,
                branch,
                current_level
            )
            VALUES (?, ?, ?)
            """,
            (
                email,
                branch,
                current_level
            )
        )

        conn.commit()

        user_id = cur.lastrowid

        # ----------------------------
        # FETCH CREATED USER
        # ----------------------------
        cur.execute(
            """
            SELECT *
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        user = cur.fetchone()

        return dict(user)

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
            SELECT *
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        user = cur.fetchone()

        return dict(user) if user else None

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
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cur.fetchone()

        return dict(user) if user else None

    finally:
        conn.close()