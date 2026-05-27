import os
import subprocess
import tempfile


def ensure_wav_16k_mono(input_path: str) -> str:
    """
    Converts any supported audio file into:
    - WAV format
    - 16kHz
    - mono channel

    Returns:
        path to converted temporary wav file
    """

    if not os.path.exists(input_path):
        raise Exception("Input audio file not found")

    # --------------------------------
    # CREATE TEMP OUTPUT
    # --------------------------------
    temp_fd, output_path = tempfile.mkstemp(
        suffix=".wav"
    )

    os.close(temp_fd)

    # --------------------------------
    # FFMPEG COMMAND
    # --------------------------------
    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        "-vn",
        output_path
    ]

    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

    except subprocess.CalledProcessError:
        raise Exception(
            "Audio conversion failed. Ensure ffmpeg is installed."
        )

    # --------------------------------
    # VALIDATE OUTPUT
    # --------------------------------
    if not os.path.exists(output_path):
        raise Exception("Converted audio file missing")

    if os.path.getsize(output_path) == 0:
        raise Exception("Converted audio file is empty")

    return output_path