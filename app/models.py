from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class Person(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30)
    Age = models.IntegerField()
    Phone = models.IntegerField()

    def __str__(self):
        return self.Name
    

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'
