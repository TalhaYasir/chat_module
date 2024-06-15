from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from channels.middleware import BaseMiddleware
from users.serializers import UserSerializer
import urllib.parse
@database_sync_to_async
def get_user(token_key):
    # If you are using normal token based authentication
    try:
        token = Token.objects.get(key=token_key)
        print(token)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token= scope['query_string'].decode('utf-8')
            _token_=urllib.parse.parse_qs(token)
            token_key=_token_.get('token', [None])[0]
            print(token_key)
            
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)
