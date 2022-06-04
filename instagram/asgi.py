# mysite/asgi.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram.settings')
django.setup()


from django.core.asgi import get_asgi_application
from chat import routing
import channels

channel_layer = channels.layers.get_channel_layer()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})