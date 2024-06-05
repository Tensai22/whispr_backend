from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from datetime import timedelta
from django.utils import timezone

class CustomUser(User):
    class Meta:
        proxy = True

CustomUser.user_permissions.field.related_name = 'custom_user_permissions'


class CustomGroup(Group):
    class Meta:
        proxy = True
        verbose_name = 'Custom Group'
        verbose_name_plural = 'Custom Groups'

CustomUser.groups.field.related_name = 'custom_user_groups'

class Profile(models.Model):
    photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default_profile_image.jpeg', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    @property
    def is_online(self):
        now = timezone.now()
        return (now - self.last_activity) < timedelta(minutes=2)

class Chat(models.Model):
    participants = models.ManyToManyField(User)

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


