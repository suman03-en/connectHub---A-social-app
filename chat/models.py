from django.db import models
from django.db.models import Q
from django.conf import settings



class Room(models.Model):
    name = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="rooms"
    )

    class Meta:
        indexes = [
            models.Index(fields=['name'],name='room_name_idx'),
        ]
    @classmethod
    def generate_room_name(cls,**kwargs):
        if kwargs:
            sender_id = str(kwargs['sender'].id)
            receiver_id = str(kwargs['receiver'].id)

            sorted_ids = sorted([sender_id,receiver_id])
            canonical_room_name = f'room-{sorted_ids[0]}-{sorted_ids[1]}'
            
            return canonical_room_name

            
    def __str__(self):
        return f"{self.name}"
    

class ChatMessage(models.Model):
    room = models.ForeignKey(
        Room,
        related_name="messages",
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="messages_sent",
        on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"R/{self.room} | {self.message[:10]} by {self.sender}"


