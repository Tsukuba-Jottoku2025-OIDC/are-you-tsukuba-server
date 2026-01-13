from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError, jwk

from api.config import (
    OIDC_ISSUER,
    OIDC_AUDIENCE,
    OIDC_ALGORITHMS,
    ENABLE_DEV_LOGIN,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)
from api.jwks import get_jwk_by_kid

bearer = HTTPBearer(auto_error=False)


async def _decode_with_oidc(token: str) -> Dict[str, Any]:
    if not OIDC_ISSUER:
        raise HTTPException(status_code=500, detail="OIDC_ISSUER is not configured")

    # header から kid を取る
    try:
        header = jwt.get_unverified_header(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token header")

    kid = header.get("kid")
    if not kid:
        raise HTTPException(status_code=401, detail="Token header missing kid")

    # issuer から JWKS を取得して kid 一致鍵で検証
    try:
        jwk_dict = await get_jwk_by_kid(kid)
    except Exception:
        raise HTTPException(status_code=401, detail="Unable to resolve signing key (kid)")

    try:
        key_obj = jwk.construct(jwk_dict)          # jose.jwk.Key
        key_pem = key_obj.to_pem().decode("utf-8") # jwt.decode で使う
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid JWK key material")

    # decode options
    kwargs: Dict[str, Any] = {
        "key": key_pem,
        "algorithms": OIDC_ALGORITHMS,
        "issuer": OIDC_ISSUER,
        "options": {
            "verify_signature": True,
            "verify_aud": bool(OIDC_AUDIENCE),
            "verify_iss": True,
            "verify_exp": True,
        },
    }
    if OIDC_AUDIENCE:
        kwargs["audience"] = OIDC_AUDIENCE

    try:
        payload = jwt.decode(token, **kwargs)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="JWT verification failed")


def _decode_dev_hs256(token: str) -> Dict[str, Any]:
    if not ENABLE_DEV_LOGIN:
        raise HTTPException(status_code=401, detail="Dev token not allowed")
    if not JWT_SECRET_KEY:
        raise HTTPException(status_code=500, detail="JWT_SECRET_KEY is not configured")

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_aud": False, "verify_iss": False},
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Dev JWT verification failed")


async def get_current_user(
    cred: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
) -> Dict[str, Any]:
    if cred is None or cred.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = cred.credentials.strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty token")

    # 優先：OIDC issuer 検証（要件）
    if OIDC_ISSUER:
        return await _decode_with_oidc(token)

    # fallback（開発のみ）
    return _decode_dev_hs256(token)
