import uuid
from django.db import models

# Create your models here.

# class Message(models.Model):
#     text = models.TextField(null=True, blank=True)
#     image = models.ImageField(upload_to='chat/image/', null=True, blank=True)
#     file = models.FileField(upload_to='chat/file/', null=True, blank=True)
#     sender = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.sender.username


class Chat(models.Model):
    class ChatType(models.TextChoices):
        GROUP = "group", "Group"
        INDIVIDUAL = "individual", "Individual"

    chat_id = models.CharField(max_length=255, unique=True)
    admin = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admins",
    )
    customer = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers",
    )
    chat_type = models.CharField(
        max_length=12, choices=ChatType.choices, default=ChatType.INDIVIDUAL
    )
    members = models.ManyToManyField("auth.User", related_name="members", blank=True)
    group = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


#     def __str__(self) -> str:
#         return self.chat_id


class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4())
    store = models.IntegerField(null=True)
    group_display_name = models.CharField(max_length=255, blank=True, null=True)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_group = models.BooleanField(default=True)

    def __str__(self):
        return str(self.room_id)
    
    def save(self,*args, **kwargs):
        if not self.group_name:        
            self.group_name = self.get_group_name()
        return super().save()
    
    def get_group_name(self):
        
        if self.group_display_name:
            group_ = "_".join(self.group_name.split(" "))
            return f"{group_}_{self.room_id}"
        
        return f"group_{self.room_id}"



class Message(models.Model):
    sender = models.IntegerField(null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(null=True)

    event_type = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender) + "--->" + str(self.room.room_id)
