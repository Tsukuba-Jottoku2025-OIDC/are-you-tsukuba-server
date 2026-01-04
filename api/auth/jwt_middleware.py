# jwt_middleware.py
# リクエストごとの検証
# 写経
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
        if self._is_exempt_path(request.path):
            return self.get_response(request)
            
        accsess_token = request.COOKIES.get(settings.ACCESS_TOKEN_KEY)

        if not accsess_token:
            return JsonResponse({
                'error': '認証が必要です',
                'code': 'NO_TOKEN' 
            },status=401)

        try:
            payload = decode_jwt(accsess_token)
            request.user_id = payload.get('user_id')

            return self.get_response(request)

        except ExpiredSignatureError:
            refresh_result = self._try_refresh_token(request)

            if refresh_result['success']:
                request.user_id = refresh_result['user_id']
                response =self.get_response(request)

                self._set_new_access_token(response,refresh_result['token'])
                return response
            
            else:
                return JsonResponse({
                    'error': refresh_result['error'],
                    'code': 'TOKEN_EXPIRED'
                },status=401)
            
        except InvalidTokenError as e:
            return JsonResponse({
                'error': '無効なトークンです',
                'code': 'INVALID_TOKEN',
                'detail': str(e)
            },status=401)
    
    def _is_exempt_path(self,path):
        return any(path.startswith(exempt) for exempt in self.exempt_paths)
    
    def _try_refresh_token(self,request):
        refresh_token =request.COOKIES.get(settings.REFRESH_TOKEN_KEY)

        if not refresh_token:
            return{
                'success': False,
                'error': 'リフレッシュトークンが見つかりません'
            }
        
        try:
            payload = decode_jwt(refresh_token)

            if payload.get('type')!= 'refresh':
                return {
                    'success': False,
                    'error': '無効なリフレッシュトークンです'
                }
            
            user_id = payload.get('user_id')
            new_access_tokeen = generate_jwt({
                {'user_id':user_id},
                settings.ACCSESS_TOKEN_LIFETIME
            })

            return {
                'success':True,
                'user_id':user_id,
                'token':new_access_tokeen
            }

        except ExpiredSignatureError:
            return {
                'success': False,
                'error': 'リフレッシュトークンの期限が切れています'
            }
        except InvalidTokenError as e:
            return {
                'success': False,
                'error': f'無効なリフレッシュトークンです:{str(e)}'
            }
        
    def _set_new_access_token(self,response,token):
        access_expiry = datetime.utcnow() + settings.ACCESS_TOKEN_LIFETIME
        response.set_cookie(
            settings.ACCESS_TOKEN_KEY,
            token,
            httponly = True,
            secure = True,
            samesite = 'Lax',
            expires = access_expiry
        )




