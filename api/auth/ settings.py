# 一旦コピペ
import datetime

SECRET_KEY = ...

# 以下を追加
JWT_SECRET_KEY = SECRET_KEY
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_KEY = 'jwt_access'
REFRESH_TOKEN_KEY = 'jwt_refresh'
ACCESS_TOKEN_LIFETIME = datetime.timedelta(minutes=5)
REFRESH_TOKEN_LIFETIME = datetime.timedelta(days=7)