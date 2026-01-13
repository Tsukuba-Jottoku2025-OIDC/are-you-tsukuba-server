from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.config import ENABLE_DEV_LOGIN
from api.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    """
    デモ用ログイン（ENABLE_DEV_LOGIN=true のときだけ使う）
    本番は IdP でログインして得たアクセストークンを使う想定。
    """
    if not ENABLE_DEV_LOGIN:
        raise HTTPException(status_code=404, detail="disabled")

    if data.username != "admin" or data.password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": "admin", "user_id": 1})
    return {"access_token": token, "token_type": "bearer"}
