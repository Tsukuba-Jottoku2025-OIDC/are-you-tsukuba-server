# コピペ
from datetime import timedelta
import os

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY','your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'

ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)

ACCESS_TOKEN_KEY = 'access_token'
REFRESH_TOKEN_KEY = 'refresh_token'

MIDDLEWARE = [
    'your_app.jwt_middleware.JWTAuthenticationMiddleware'
]