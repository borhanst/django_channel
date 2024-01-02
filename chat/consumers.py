import json
import uuid
from chat.serializers import MessageSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message, Room
from channels.db import database_sync_to_async


@database_sync_to_async
def get_or_create_room(chat_id: str):
    room, _ = Room.objects.get_or_create(room_id=chat_id)
    return room


@database_sync_to_async
def create_message(data: dict):
    return Message.objects.create(**data)


class ChatAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        print(self.user)
        if not self.user.is_authenticated:
            self.close()
            return

        self.kwargs = self.scope["url_route"]["kwargs"]
        self.room = self.kwargs.get("room")
        if not self.room:
            self.room = uuid.uuid4()
        self.room_obj = await get_or_create_room(self.room)
        self.group_name = f"chat_{self.room}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("connected......")
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print("message received", text_data, bytes_data)
        data = json.loads(text_data)
        print(data)
        payload = {"body": data.get('body'), "event_type": data.get('event_type'), "sender": 1, "room": self.room_obj}

        message = await create_message(data=payload)
        message_serializer = MessageSerializer(message)
        # print(message_serializer.data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": data.get('event_type'),
                "data": message_serializer.data,
            },
        )


    async def chat_message(self, event):
        print("send..", event)
        await self.send(text_data=json.dumps(event))
        
    
    async def add_member(self, event):
        
        print("add member", event)



    async def disconnect(self, code):
        self.user = self.scope.get("user")
        print(self.user)
        if self.user.is_authenticated:
            await self.send(
                text_data=json.dumps(
                    {"type": "user.unauthorized", "message": "user not login"}
                )
            )
            print("send close message")
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            print("dis connect", code)
        self.close()
