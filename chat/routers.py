from django.urls import path
from chat.consumers import ChatAsyncWebsocketConsumer

websocket_urlpatterns = [
    path("send/<str:room_id>/", ChatAsyncWebsocketConsumer.as_asgi())
]