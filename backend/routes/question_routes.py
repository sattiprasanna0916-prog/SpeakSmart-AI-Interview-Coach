from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
from backend.ai.question_generator import generate_question, generate_followup_question
router = APIRouter(prefix="/question", tags=["Question"])


class QuestionRequest(BaseModel):
    level: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
class FollowupRequest(BaseModel):
    previous_question: str = Field(..., min_length=3)
    user_answer: str = Field(..., min_length=3)
    role: str = Field(..., min_length=1)
    hint: str = ""
@router.post("/generate")
def generate_question_api(req: QuestionRequest):
    try:
        question = generate_question(
            level=req.level,
            category=req.category,
            role=req.role
        )

        return {
            "status": "success",
            "question": question
        }

    except Exception as e:
        print("[Question API Error]:", e)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate question"
        )
@router.post("/followup")
def generate_followup_api(req: FollowupRequest):
    try:
        question = generate_followup_question(
            previous_question=req.previous_question,
            user_answer=req.user_answer,
            role=req.role,
            hint=req.hint
        )

        return {
            "status": "success",
            "question": question
        }

    except Exception as e:
        print("[Followup API Error]:", e)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate follow-up question"
        )