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

class Chat(models.Model):
    participants = models.ManyToManyField(User)

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


