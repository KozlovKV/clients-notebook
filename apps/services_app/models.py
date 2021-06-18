from django.contrib.auth.models import User
from django.db import models


class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    label = models.CharField(max_length=255)
    description = models.TextField()
