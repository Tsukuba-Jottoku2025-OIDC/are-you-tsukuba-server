from fastapi import APIRouter, Depends
from api.auth.deps import get_current_user

router = APIRouter(tags=["protected"])


@router.get("/protected/")
async def protected(user=Depends(get_current_user)):
    return {"message": "JWT OK", "user": user}
