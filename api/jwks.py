from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple

import httpx

from api.config import OIDC_ISSUER, OIDC_DISCOVERY_CACHE_TTL, JWKS_CACHE_TTL


# ---- simple in-memory caches (good enough for single-container) ----
_discovery_cache: Optional[Tuple[float, Dict[str, Any]]] = None  # (expires_at, data)
_jwks_cache: Optional[Tuple[float, Dict[str, Any]]] = None       # (expires_at, jwks)


def _now() -> float:
    return time.time()


async def fetch_openid_configuration() -> Dict[str, Any]:
    """
    OpenID Discovery:
      GET {issuer}/.well-known/openid-configuration
    """
    global _discovery_cache
    if _discovery_cache and _discovery_cache[0] > _now():
        return _discovery_cache[1]

    if not OIDC_ISSUER:
        raise RuntimeError("OIDC_ISSUER is not set")

    url = OIDC_ISSUER.rstrip("/") + "/.well-known/openid-configuration"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()

    _discovery_cache = (_now() + OIDC_DISCOVERY_CACHE_TTL, data)
    return data


async def fetch_jwks() -> Dict[str, Any]:
    """
    JWKS:
      discovery.jwks_uri を参照して GET
    """
    global _jwks_cache
    if _jwks_cache and _jwks_cache[0] > _now():
        return _jwks_cache[1]

    conf = await fetch_openid_configuration()
    jwks_uri = conf.get("jwks_uri")
    if not jwks_uri:
        raise RuntimeError("jwks_uri not found in openid-configuration")

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(jwks_uri)
        r.raise_for_status()
        jwks = r.json()

    _jwks_cache = (_now() + JWKS_CACHE_TTL, jwks)
    return jwks


async def get_jwk_by_kid(kid: str) -> Dict[str, Any]:
    jwks = await fetch_jwks()
    keys = jwks.get("keys", [])
    for k in keys:
        if k.get("kid") == kid:
            return k
    # kid が見つからない → 鍵更新の可能性があるので cache を捨てて再取得して再探索
    global _jwks_cache
    _jwks_cache = None
    jwks = await fetch_jwks()
    keys = jwks.get("keys", [])
    for k in keys:
        if k.get("kid") == kid:
            return k
    raise KeyError(f"JWK not found for kid={kid}")
