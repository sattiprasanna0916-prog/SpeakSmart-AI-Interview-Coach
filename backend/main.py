
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text

from backend.db import engine

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
    version="2.0.0"
)

# --------------------------------
# DATABASE INITIALIZATION
# --------------------------------
def init_db():

    with engine.connect() as conn:

        # USERS TABLE
        conn.execute(text("""

        CREATE TABLE IF NOT EXISTS users (

            user_id SERIAL PRIMARY KEY,

            email VARCHAR(255) UNIQUE,

            branch VARCHAR(255),

            current_level VARCHAR(50)

        )

        """))

        # ATTEMPTS TABLE
        conn.execute(text("""

        CREATE TABLE IF NOT EXISTS attempts (

            id SERIAL PRIMARY KEY,

            user_id INTEGER,

            level VARCHAR(50),

            question TEXT,

            answer_text TEXT,

            audio_duration FLOAT,

            pause_count INTEGER,

            filler_count INTEGER,

            speech_rate FLOAT,

            fluency_score FLOAT,

            grammar_score FLOAT,

            accuracy_score FLOAT,

            final_score FLOAT,

            feedback TEXT,

            improved_answer TEXT,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )

        """))

        conn.commit()

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

        "message": "SpeakSmart PostgreSQL backend running 🚀"
    }
