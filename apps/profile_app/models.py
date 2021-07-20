from django.contrib.auth.models import User
import apps.services_app.models as services_models

from django.db import models
from django.urls import reverse_lazy


class UserAdditionInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()
    avatar = models.ImageField(upload_to='users_avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user} - addition'

    def get_absolute_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.pk})

    def get_avatar_url(self):
        try:
            return self.avatar.url
        except ValueError:
            return ''

    @property
    def services(self):
        return services_models.Service.objects.filter(provider=self.user)

    @property
    def service_notes(self):
        notes = []
        for service in self.services:
            notes += services_models.ServiceNote.objects.filter(service=service)
        return notes
