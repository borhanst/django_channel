from django.contrib import admin
from chat.models import Chat, Message, Room
# Register your models here.

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Room)