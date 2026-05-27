import os
import re
from groq import Groq


MODEL_NAME = "llama-3.1-8b-instant"


def clean_bullets(text: str):
    lines = text.split("\n")

    cleaned = []

    for line in lines:
        line = line.strip()

        line = re.sub(
            r"^[\-\*\d\.\)\s]+",
            "",
            line
        )

        if line:
            cleaned.append(line)

    return "\n".join(cleaned[:4])


def generate_feedback_groq(
    transcript: str,
    fluency: float,
    grammar: float,
    accuracy: float,
    question: str = "",
    expected_text: str = "",
    role: str = "Candidate",
    **kwargs
):
    """
    Generates:
    - professional interview feedback
    - improved interview answer
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY not set")

    client = Groq(api_key=api_key)

    # --------------------------------
    # FEEDBACK PROMPT
    # --------------------------------
    feedback_prompt = f"""
You are a senior technical interviewer and communication coach.

Analyze the candidate's interview response.

Interview Question:
{question}

Candidate Answer:
{transcript}

Evaluation Scores (0-10):
- Fluency: {fluency}
- Grammar: {grammar}
- Accuracy: {accuracy}

Your task:
1. Identify communication weaknesses
2. Identify technical/content weaknesses
3. Suggest actionable improvements
4. Keep feedback concise and professional

Rules:
- Give exactly 3 bullet points
- Be constructive
- Avoid generic advice
- Focus on interview performance
- Maximum 90 words total
"""

    feedback_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert interview evaluator."
                )
            },
            {
                "role": "user",
                "content": feedback_prompt
            }
        ],
        temperature=0.5,
        max_tokens=180,
    )

    raw_feedback = (
        feedback_response
        .choices[0]
        .message.content or ""
    ).strip()

    feedback = clean_bullets(raw_feedback)

    # --------------------------------
    # IMPROVED ANSWER PROMPT
    # --------------------------------
    improve_prompt = f"""
You are helping a candidate improve an interview response.

Interview Question:
{question}

Original Answer:
{transcript}

Rewrite the answer professionally.

Requirements:
- Natural spoken English
- Confident tone
- Clear structure
- Technically relevant
- 4-6 sentences
- Sound like a real interview answer
- Do NOT use bullet points
- Do NOT add labels
"""

    improve_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You improve interview answers professionally."
                )
            },
            {
                "role": "user",
                "content": improve_prompt
            }
        ],
        temperature=0.6,
        max_tokens=220,
    )

    improved_answer = (
        improve_response
        .choices[0]
        .message.content or ""
    ).strip()

    return {
        "feedback": feedback,
        "improved_answer": improved_answer,
    }