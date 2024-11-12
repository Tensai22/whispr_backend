from django.db import models

class Message(models.Model):
    room_name = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_name}: {self.message}"