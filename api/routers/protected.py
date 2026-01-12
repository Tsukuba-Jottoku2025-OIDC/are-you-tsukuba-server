from fastapi import APIRouter, Depends
from api.auth.deps import get_current_user

router = APIRouter(prefix="/protected", tags=["protected"])

@router.get("/")
def protected(user_id: int = Depends(get_current_user)):
    return {"message": "JWT OK", "user_id": user_id}
