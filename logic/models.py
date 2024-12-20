from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Profile(models.Model):
    photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default_profile_image.jpeg', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username