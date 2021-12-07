import os
import uuid

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


def user_directory_path(instance, filename, ):
    path = 'user_{0}/profile_{1}.jpg'.format(instance.user.id, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(full_path):
        os.remove(full_path)
    return path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=100)
    email = models.EmailField()
    picture = models.ImageField(upload_to=user_directory_path)

    def save(self, *args, **kwargs):
        photo = super().save(*args, **kwargs)
        SIZE = 250, 250
        print(photo)
        if self.picture:
            print(self.picture.path)
            pic = Image.open(self.picture.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.picture.path)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse()
