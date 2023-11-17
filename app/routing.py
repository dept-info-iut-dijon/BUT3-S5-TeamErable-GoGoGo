from django.urls import re_path, path

from .channels.GameJoinAndLeave import GameJoinAndLeave

websocket_urlpatterns = [
    path('game/<int:game_id>/', GameJoinAndLeave.as_asgi()),
]
