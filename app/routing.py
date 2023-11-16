from django.urls import re_path, path

from .channels.Consumers import JoinAndLeave

websocket_urlpatterns = [
    path('game/<int:game_id>/', JoinAndLeave.as_asgi()),
]
