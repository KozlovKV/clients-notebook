from django.contrib.auth.models import User
from django.db import models
from django.core import validators

import apps.services_app.models as services_models


class UserAdditionInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()
    avatar = models.ImageField(upload_to='users_avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user} - addition'


class Feedback(models.Model):
    service_note = models.ForeignKey(services_models.ServiceNote, on_delete=models.DO_NOTHING)
    mark = models.IntegerField(
        validators=[
            validators.MinValueValidator(0), validators.MaxValueValidator(10)
        ]
    )
    text = models.TextField()

    def __str__(self):
        return f'Feedback on {self.service_note} ({self.mark}/10)'
