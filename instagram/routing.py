from channels.auth import AuthMiddleWareStack
from channels.routing import ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator({
        AuthMiddleWareStack(

        )
    }),
    # Just HTTP for now. (We can add other protocols later.)
})