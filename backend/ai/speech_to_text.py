import os
from groq import Groq


MODEL_NAME = "whisper-large-v3"


def transcribe_audio(audio_path: str) -> str:
    """
    Converts speech audio into text
    using Groq Whisper API.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY not set")

    client = Groq(api_key=api_key)

    try:
        # --------------------------------
        # VALIDATION
        # --------------------------------
        if not os.path.exists(audio_path):
            raise Exception("Audio file not found")

        if os.path.getsize(audio_path) == 0:
            raise Exception("Empty audio file")

        # --------------------------------
        # TRANSCRIPTION
        # --------------------------------
        with open(audio_path, "rb") as audio_file:

            response = client.audio.transcriptions.create(
                file=audio_file,
                model=MODEL_NAME,
                response_format="json",
                language="en",
                temperature=0.0
            )

        transcript = (
            getattr(response, "text", "") or ""
        ).strip()

        # --------------------------------
        # CLEAN RESPONSE
        # --------------------------------
        transcript = transcript.replace("\n", " ")

        return transcript

    except Exception as e:
        print("Speech-to-text error:", e)
        return ""