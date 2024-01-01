import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Chat, Message
from channels.db import database_sync_to_async


@database_sync_to_async
def get_or_create_chat(chat_id: str):
    return Chat.objects.get_or_create(chat_id=chat_id)


@database_sync_to_async
def create_message(data:dict):
    Message.objects.create(**data)
    


class ChatAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        self.kwargs = self.scope["url_route"]["kwargs"]
        self.room = self.kwargs.get("room")
        if not self.room:
            self.room = str(uuid.uuid4())[0:6]
        self.group_name = f"chat_{self.room}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("connected......")
        await self.accept()
        

    async def receive(self, text_data=None, bytes_data=None):
        print("message received", text_data, bytes_data)
        data = json.loads(text_data)
        payload = {
            'body': data.get("message"),
            'sender': 1,
            'store':2,
            'room': self.room
        }
        await create_message(data=payload)
        await self.channel_layer.group_send(
            self.group_name, {"type": "chat.message", "data": json.dumps({
            'body': data.get("message"),
            'room': self.room
        })}
        )
        
        

    async def chat_message(self, event):
        print("send..", event)
        await self.send(text_data=json.dumps(event))
        
    

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("dis connect", code)
        
