import os
import httpx
from groq import Groq


MODEL_NAME = "llama-3.1-8b-instant"

api_key = os.getenv("GROQ_API_KEY")

http_client = httpx.Client(timeout=25.0)

client = Groq(
    api_key=api_key,
    http_client=http_client
)


def generate_question(level: str, category: str, role: str):
    """
    Generates realistic interview questions
    based on:
    - role
    - category
    - difficulty level
    """

    if not api_key:
        raise Exception("GROQ_API_KEY not set")

    difficulty_map = {
        "Beginner": "easy entry-level",
        "Intermediate": "moderate industry-level",
        "Advanced": "challenging senior-level"
    }

    difficulty = difficulty_map.get(
        level,
        "moderate industry-level"
    )

    prompt = f"""
You are a professional interviewer conducting a real interview.

Generate ONE interview question.

Candidate Role:
{role}

Interview Type:
{category}

Difficulty:
{difficulty}

Rules:
- Ask only ONE question
- Make it realistic
- Keep it concise
- Avoid explanations
- Avoid numbering
- Should sound natural in a real interview
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced interviewer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8,
        max_tokens=80,
    )

    question = (
        response.choices[0]
        .message.content or ""
    ).strip()

    return question


def generate_followup_question(
    previous_question: str,
    user_answer: str,
    role: str,
    hint: str = ""
):
    """
    Generates intelligent follow-up questions
    based on candidate response.
    """

    if not api_key:
        raise Exception("GROQ_API_KEY not set")

    prompt = f"""
You are a senior interviewer.

Previous Interview Question:
{previous_question}

Candidate Answer:
{user_answer}

Guidance:
{hint}

Your task:
Ask ONE intelligent follow-up question.

Rules:
- Question must relate to candidate response
- Dig deeper into reasoning or experience
- Sound conversational
- No explanations
- No numbering
- Keep under 25 words
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert interviewer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=60,
    )

    followup = (
        response.choices[0]
        .message.content or ""
    ).strip()

    return followup