from rest_framework import serializers
from chat.models import Room, Message


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'room', 'body']