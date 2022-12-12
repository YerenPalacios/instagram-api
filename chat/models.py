from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class ChatRoom(models.Model): 
    users = models.ManyToManyField(get_user_model())
    is_group = models.BooleanField(default=False)
    
class ChatRoomMessage(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content