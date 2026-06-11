from django.db import models
from django.conf import settings

# Create your models here.

class ChatRoom(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='buyer_rooms')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='seller_rooms')
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room{self.id}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

