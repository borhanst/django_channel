from channels.generic.websocket import AsyncWebsocketConsumer


class ChatAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print("connected......")
        return await super().connect()
    
    
    async def receive(self, text_data=None, bytes_data=None):
        print("message received", text_data, bytes_data)
        return await super().receive(text_data, bytes_data)
    
    
    async def disconnect(self, code):
        print("dis connect", code)
        return await super().disconnect(code)