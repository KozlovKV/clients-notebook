from django.contrib.auth.models import User
from django.db import models


class UserAdditionInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()
    avatar = models.ImageField(upload_to='users_avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user} - addition'
