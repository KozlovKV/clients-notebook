from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy


class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    label = models.CharField(max_length=255)
    image = models.ImageField(upload_to='services_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.label} by {self.provider}'

    def get_absolute_url(self):
        return reverse_lazy('one_service_calendar', kwargs={'pk': self.pk})

    def get_image_url(self):
        try:
            return self.image.url
        except ValueError:
            return ''


class ServiceNote(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()

    EMPTY = 0
    OCCUPIED = 1
    ENDED = 2
    CANCELED = 3
    STATUS_CHOICES = (
        (EMPTY, 'Свободно'),
        (OCCUPIED, 'Заято'),
        (ENDED, 'Прошло'),
        (CANCELED, 'Отменено'),
    )
    status = models.IntegerField(default=EMPTY, choices=STATUS_CHOICES)

    @property
    def status_name(self):
        for status_pair in self.STATUS_CHOICES:
            if status_pair[0] == self.status:
                return status_pair[1]

    def __str__(self):
        return f'{self.service} for {self.client} at {self.date}, {self.time_start}-{self.time_end} ' \
               f'({self.status_name})'
