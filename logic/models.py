from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Profile(models.Model):
    photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default_profile_image.jpeg', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    @property
    def is_online(self):
        now = timezone.now()
        if now - self.last_activity < timedelta(minutes=2):
            return True
        return False



class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]} - {self.timestamp}"
