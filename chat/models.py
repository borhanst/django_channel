from django.db import models

# Create your models here.

class Message(models.Model):
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat/image/', null=True, blank=True)
    file = models.FileField(upload_to='chat/file/', null=True, blank=True)
    sender = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.sender.username
    
    

class Chat(models.Model):
    class ChatType(models.TextChoices):
        GROUP = 'group', 'Group'
        INDIVIDUAL = 'individual', 'Individual'
    chat_id = models.CharField(max_length=255, unique=True)
    admin = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="admins")
    customer = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="customers")
    chat_type = models.CharField(max_length=12, choices=ChatType.choices, default=ChatType.INDIVIDUAL)
    message = models.ManyToManyField(Message, related_name='messages')
    members = models.ManyToManyField('auth.User', related_name='members', blank=True)
    group = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.chat_id
    
    