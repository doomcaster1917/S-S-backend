from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('', consumers.JoinAndLeave.as_asgi()),
    path('groups/<int:group_id>/',consumers.GroupConsumer.as_asgi())
]