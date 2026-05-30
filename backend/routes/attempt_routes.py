from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Depends
)

import os
import tempfile

from backend.services.auth_service import (
    verify_token
)

# --------------------------------
# AI MODULES
# --------------------------------
from backend.ai.audio_convert import (
    ensure_wav_16k_mono
)

from backend.ai.speech_to_text import (
    transcribe_audio
)

from backend.ai.feedback_llm import (
    generate_feedback_groq
)

from backend.ai.speech_metrics import (
    compute_audio_metrics
)

from backend.ai.grammar_score import (
    compute_grammar_score
)

from backend.ai.accuracy_score import (
    compute_accuracy_details
)

# --------------------------------
# SERVICES
# --------------------------------
from backend.services.attempt_service import (
    save_attempt,
    get_user_attempts
)

from backend.services.user_service import (
    get_user
)

from backend.services.evaluation_service import (
    evaluate_and_update_level
)


router = APIRouter(
    prefix="/attempts",
    tags=["Attempts"]
)


# --------------------------------
# CONFIG
# --------------------------------
ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".webm"
}

MAX_FILE_SIZE = 10 * 1024 * 1024

FLUENCY_WEIGHT = 0.3
GRAMMAR_WEIGHT = 0.3
ACCURACY_WEIGHT = 0.4


# --------------------------------
# SUBMIT INTERVIEW ATTEMPT
# --------------------------------
@router.post("/submit")
async def submit_attempt(
    level: str = Form(...),
    question: str = Form(...),
    audio: UploadFile = File(...),
    token_data: dict = Depends(verify_token),
):

    temp_input_path = None
    wav_path = None

    # --------------------------------
    # AUTH VALIDATION
    # --------------------------------
    user_id = token_data.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    try:
        user_id = int(user_id)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    try:

        # --------------------------------
        # FILE VALIDATION
        # --------------------------------
        filename = (
            audio.filename or ""
        ).lower()

        extension = os.path.splitext(
            filename
        )[-1]

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported audio format"
            )

        content = await audio.read()

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File size exceeds 10MB"
            )

        # --------------------------------
        # SAVE TEMP FILE
        # --------------------------------
        suffix = extension if extension else ".wav"

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(content)

            temp_input_path = temp_file.name

        # --------------------------------
        # AUDIO CONVERSION
        # --------------------------------
        wav_path = ensure_wav_16k_mono(
            temp_input_path
        )

        # --------------------------------
        # SPEECH TO TEXT
        # --------------------------------
        transcript = (
            transcribe_audio(wav_path) or ""
        ).strip()

        if (
            not transcript or
            transcript.lower() in [
                "silence",
                "no speech detected"
            ]
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "No clear speech detected. "
                    "Please speak clearly."
                )
            )

        # --------------------------------
        # AUDIO METRICS
        # --------------------------------
        metrics = compute_audio_metrics(
            wav_path,
            transcript
        )

        audio_duration = float(
            metrics.get("audio_duration", 0)
        )

        if audio_duration < 2.5:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Audio too short. "
                    "Minimum 3 seconds required."
                )
            )

        # --------------------------------
        # FLUENCY
        # --------------------------------
        fluency = float(
            metrics.get("fluency_score", 0)
        )

        # --------------------------------
        # GRAMMAR
        # --------------------------------
        grammar = float(
            compute_grammar_score(transcript)
        )

        # --------------------------------
        # ACCURACY
        # --------------------------------
        accuracy_details = (
            compute_accuracy_details(
                transcript,
                question
            )
        )

        accuracy = float(
            accuracy_details.get("score", 0)
        )

        # --------------------------------
        # FINAL SCORE
        # --------------------------------
        final_score = round(
            (
                fluency * FLUENCY_WEIGHT
            ) +
            (
                grammar * GRAMMAR_WEIGHT
            ) +
            (
                accuracy * ACCURACY_WEIGHT
            ),
            2
        )

        # --------------------------------
        # AI FEEDBACK
        # --------------------------------
        feedback_response = (
            generate_feedback_groq(
                transcript=transcript,
                fluency=fluency,
                grammar=grammar,
                accuracy=accuracy,
                question=question,
            )
        )

        feedback = feedback_response.get(
            "feedback",
            ""
        )

        improved_answer = (
            feedback_response.get(
                "improved_answer",
                ""
            )
        )

        # --------------------------------
        # IMPROVEMENT TRACKING
        # --------------------------------
        previous_attempts = (
            get_user_attempts(user_id)
        )

        previous_score = None

        if previous_attempts:
            previous_score = (
                previous_attempts[0]
                .get("final_score")
            )

        improvement = 0

        if previous_score is not None:
            improvement = round(
                final_score -
                float(previous_score),
                2
            )

        # --------------------------------
        # SAVE ATTEMPT
        # --------------------------------
        save_attempt(
            user_id=user_id,
            level=level,
            question=question,
            answer_text=transcript,

            audio_duration=metrics.get(
                "audio_duration",
                0
            ),

            pause_count=metrics.get(
                "pause_count",
                0
            ),

            filler_count=metrics.get(
                "filler_count",
                0
            ),

            speech_rate=metrics.get(
                "speech_rate",
                0
            ),

            fluency_score=fluency,
            grammar_score=grammar,
            accuracy_score=accuracy,

            final_score=final_score,

            feedback=feedback,

            improved_answer=improved_answer,
        )

        # --------------------------------
        # LEVEL UPDATE
        # --------------------------------
        level_update = (
            evaluate_and_update_level(
                user_id
            )
        )

        # --------------------------------
        # RESPONSE
        # --------------------------------
        return {
            "status": "success",

            "transcript": transcript,

            "scores": {
                "fluency": round(fluency, 2),
                "grammar": round(grammar, 2),
                "accuracy": round(accuracy, 2),
                "final_score": final_score,
            },

            "improvement": improvement,

            "feedback": feedback,

            "improved_answer": improved_answer,

            "audio_metrics": metrics,

            "level_update": level_update,
        }

    finally:

        # --------------------------------
        # CLEANUP
        # --------------------------------
        if (
            temp_input_path and
            os.path.exists(temp_input_path)
        ):
            os.remove(temp_input_path)

        if (
            wav_path and
            os.path.exists(wav_path)
        ):
            os.remove(wav_path)


# --------------------------------
# GET USER ATTEMPTS
# --------------------------------
@router.get("/user/{user_id}")
def get_attempts(
    user_id: int,
    token_data: dict = Depends(verify_token)
):

    token_user = token_data.get("sub")

    if str(user_id) != str(token_user):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    user = get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    attempts = get_user_attempts(user_id)

    return {
        "status": "success",
        "attempts": attempts
    }