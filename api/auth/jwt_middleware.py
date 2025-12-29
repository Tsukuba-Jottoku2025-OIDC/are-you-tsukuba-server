# jwt_middleware.py
# リクエストごとの検証
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from .jwt_utils import decode_jwt, generate_jwt

class JWTAuthenticationMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        # 認証不要なパスのリスト
        self.exempt_paths = [
            '/api/auth/login',
            '/api/auth/register',
            '/api/auth/logout',
            '/admin/',
        ]

        def __call__(self, request):
            pass