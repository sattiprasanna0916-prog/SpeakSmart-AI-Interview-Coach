from fastapi import APIRouter,HTTPException
from backend.services.progress_service import compute_progress
from backend.services.user_service import get_user
router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/user/{user_id}")
def get_progress(user_id: int):

    user = get_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    progress = compute_progress(user_id)

    return {
        "status": "success",
        "data": progress
    }