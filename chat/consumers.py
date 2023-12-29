import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Chat, Message
from channels.db import database_sync_to_async


@database_sync_to_async
def get_or_create_chat(chat_id: str):
    return Chat.objects.get_or_create(chat_id=chat_id)


@database_sync_to_async
def create_message(text, sender, room_id):
    message = Message.objects.create(text=text, sender=sender)
    chat = Chat.objects.get(chat_id=room_id)
    chat.message.add(message)


class ChatAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        self.kwargs = self.scope["url_route"]["kwargs"]
        self.room_id = self.kwargs.get("room_id")
        self.group_name = f"chat_{self.room_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("connected......")
        return await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        print("message received", text_data, bytes_data)
        data = json.loads(text_data)
        await create_message(data.get("message"), self.user, self.room_id)
        await self.channel_layer.group_send(
            self.group_name, {"type": "chat.message", "data": text_data}
        )
        return await super().receive(text_data, bytes_data)

    async def chat_message(self, event):
        print("send..", event)
        await self.send(text_data=event["data"])

    async def disconnect(self, code):
        print("dis connect", code)
        return await super().disconnect(code)
