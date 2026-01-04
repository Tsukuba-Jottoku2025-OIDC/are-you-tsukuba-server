# views.py
# ログイン・ログアウトなどのビュー
# コピペ

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .jwt_utils import create_token_response, delete_token_response


# ==================================================
# 認証エンドポイント（認証不要）
# ==================================================

@require_http_methods(["POST"])
def login_view(request):
    """
    ログイン処理
    POST /api/auth/login
    Body: username=alice&password=secret123
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if not username or not password:
        return JsonResponse({'error': '必須項目が不足しています'}, status=400)
    
    user = authenticate(username=username, password=password)
    
    if user:
        return create_token_response(user.id, 'ログイン成功')
    else:
        return JsonResponse({
            'error': 'ユーザー名またはパスワードが正しくありません'
        }, status=401)


@require_http_methods(["POST"])
def logout_view(request):
    """
    ログアウト処理
    POST /api/auth/logout
    """
    return delete_token_response('ログアウトしました')


# ==================================================
# ユーザー管理エンドポイント（認証必要）
# ==================================================

@require_http_methods(["GET"])
def user_profile_view(request):
    """
    プロフィール取得
    GET /api/user/profile
    request.user_id はミドルウェアで設定済み
    """
    try:
        user = User.objects.get(id=request.user_id)
        return JsonResponse({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'ユーザーが見つかりません'}, status=404)


@require_http_methods(["PUT", "PATCH"])
def update_profile_view(request):
    """
    プロフィール更新
    PUT /api/user/profile
    """
    try:
        user = User.objects.get(id=request.user_id)
        
        if request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
        if request.POST.get('last_name'):
            user.last_name = request.POST.get('last_name')
        if request.POST.get('email'):
            user.email = request.POST.get('email')
        
        user.save()
        
        return JsonResponse({
            'message': 'プロフィールを更新しました',
            'user': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'ユーザーが見つかりません'}, status=404)


@require_http_methods(["DELETE"])
def delete_account_view(request):
    """
    アカウント削除
    DELETE /api/user/account
    """
    try:
        user = User.objects.get(id=request.user_id)
        username = user.username
        user.delete()
        
        return delete_token_response(f'アカウント {username} を削除しました')
    except User.DoesNotExist:
        return JsonResponse({'error': 'ユーザーが見つかりません'}, status=404)


@require_http_methods(["GET"])
def check_auth_view(request):
    """
    認証状態確認
    GET /api/auth/check
    このエンドポイントに到達できれば認証済み
    """
    return JsonResponse({
        'authenticated': True,
        'user_id': request.user_id
    })