from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import get_connection

# --------------------------------
# ROUTES
# --------------------------------
from backend.routes.user_routes import (
    router as user_routes
)

from backend.routes.question_routes import (
    router as question_routes
)

from backend.routes.attempt_routes import (
    router as attempt_routes
)

from backend.routes.progress_routes import (
    router as progress_routes
)


# --------------------------------
# FASTAPI APP
# --------------------------------
app = FastAPI(
    title="SpeakSmart API",
    version="1.0.0"
)


# --------------------------------
# DATABASE INITIALIZATION
# --------------------------------
def init_db():

    conn = get_connection()
    cur = conn.cursor()

    try:

        # ----------------------------
        # USERS TABLE
        # ----------------------------
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                branch TEXT,
                current_level TEXT
            )
            """
        )

        # ----------------------------
        # ATTEMPTS TABLE
        # ----------------------------
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER,

                level TEXT,

                question TEXT,

                answer_text TEXT,

                audio_duration REAL,

                pause_count INTEGER,

                filler_count INTEGER,

                speech_rate REAL,

                fluency_score REAL,

                grammar_score REAL,

                accuracy_score REAL,

                final_score REAL,

                feedback TEXT,

                improved_answer TEXT,

                created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()

    finally:
        conn.close()


# --------------------------------
# INITIALIZE DATABASE
# --------------------------------
init_db()


# --------------------------------
# CORS
# --------------------------------
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",

        "https://english-ai-tutor-three.vercel.app"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# --------------------------------
# REGISTER ROUTES
# --------------------------------
app.include_router(user_routes)

app.include_router(question_routes)

app.include_router(attempt_routes)

app.include_router(progress_routes)


# --------------------------------
# ROOT ENDPOINT
# --------------------------------
@app.get("/")
def root():

    return {
        "status": "success",
        "message": "SpeakSmart backend running"
    }