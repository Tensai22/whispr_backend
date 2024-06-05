from django.conf import settings
from django.db import models

from logic.models import CustomUser


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
