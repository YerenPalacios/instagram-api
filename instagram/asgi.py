# mysite/asgi.py
import os
from django.core.asgi import get_asgi_application
asgi =  get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram.settings")

application = ProtocolTypeRouter({
    "http":asgi,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})
