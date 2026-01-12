from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    # 簡易認証（デモ用）
    if data.username != "admin" or data.password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": 1})
    return {"access_token": token}
