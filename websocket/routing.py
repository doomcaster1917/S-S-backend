from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('groups/<int:owner_id>/',consumers.GroupConsumer.as_asgi()),
    path('home', consumers.HomeWebSocket.as_asgi()),
]