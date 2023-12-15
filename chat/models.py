from django.db import models
from instagram_app.models import User

# Create your models here.

class ChatRoom(models.Model): 
    users = models.ManyToManyField(User)
    is_group = models.BooleanField(default=False)
    
class ChatRoomMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_post = models.BooleanField(default=False)

    def __str__(self):
        return self.content