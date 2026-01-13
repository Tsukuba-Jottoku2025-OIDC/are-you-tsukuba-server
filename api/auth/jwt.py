from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt

from api.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRES_MINUTES


def create_access_token(payload: Dict[str, Any]) -> str:
    """
    開発用のローカルトークン発行（HS256想定）。
    本番は OIDC の issuer 発行トークンを使うので、ENABLE_DEV_LOGIN=false 推奨。
    """
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not set for dev login")

    to_encode = dict(payload)
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
