from django.urls import path
from chat.consumers import ChatAsyncWebsocketConsumer

websocket_urlpatterns = [
    path("send/<str:room>/", ChatAsyncWebsocketConsumer.as_asgi()),
    path("send/", ChatAsyncWebsocketConsumer.as_asgi()),
]