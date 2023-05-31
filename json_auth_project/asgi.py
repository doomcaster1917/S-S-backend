from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'json_auth_project.settings')

asgi_application = get_asgi_application()

import websocket.routing

application = ProtocolTypeRouter({
  "http": asgi_application,
  "websocket":
  AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket.routing.websocket_urlpatterns
            )
    ),
)})
