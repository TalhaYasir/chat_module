import os
import django
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator  # new
django.setup()
from django.core.asgi import get_asgi_application
from chat import routings
from ._middleware import TokenAuthMiddleware  # new


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatAPI.settings')
print("settings ------------------------")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator( 
        TokenAuthMiddleware(URLRouter(routings.websocket_urlpatterns)))
})