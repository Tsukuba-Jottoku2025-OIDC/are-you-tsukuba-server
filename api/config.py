import os
from dotenv import load_dotenv

load_dotenv()

def _get(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

# OIDC / JWT verify
OIDC_ISSUER = _get("OIDC_ISSUER")
OIDC_AUDIENCE = _get("OIDC_AUDIENCE")  # 空なら aud 検証はスキップ
OIDC_ALGORITHMS = [x.strip() for x in _get("OIDC_ALGORITHMS", "RS256").split(",") if x.strip()]

# caching
OIDC_DISCOVERY_CACHE_TTL = int(_get("OIDC_DISCOVERY_CACHE_TTL", "3600"))
JWKS_CACHE_TTL = int(_get("JWKS_CACHE_TTL", "3600"))

# dev login (optional)
ENABLE_DEV_LOGIN = _get("ENABLE_DEV_LOGIN", "false").lower() in ("1", "true", "yes", "on")
JWT_SECRET_KEY = _get("JWT_SECRET_KEY", "")
JWT_ALGORITHM = _get("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_MINUTES = int(_get("JWT_EXPIRES_MINUTES", "60"))
