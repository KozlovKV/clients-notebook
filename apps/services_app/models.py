import datetime

from django.urls import reverse_lazy
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import User
from django.db import models


class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.SET(-1))
    label = models.CharField(max_length=255)
    image = models.ImageField(upload_to='services_images/', blank=True, null=True)
    description = models.TextField()

    ALL = 0
    AUTHORIZED = 1
    ONLY_PROVIDER = 2
    PERMISSION_CHOICES = (
        (ALL, 'Все'),
        (AUTHORIZED, 'Авторизованные'),
        (ONLY_PROVIDER, 'Только я'),
    )
    PERMISSION_CHECKERS = {
        ALL: lambda *args: True,
        AUTHORIZED: lambda *args: args[0].is_authenticated,
        ONLY_PROVIDER: lambda *args: args[0] == args[1].provider,
    }
    CAN_SEE_FIELD = 0
    who_can_see = models.IntegerField(default=ALL, choices=PERMISSION_CHOICES)
    CAN_RECORD_FIELD = 1
    who_can_record = models.IntegerField(default=ALL, choices=PERMISSION_CHOICES)
    PERMISSION_FIELDS_GETTERS = {
        CAN_SEE_FIELD: lambda self: self.who_can_see,
        CAN_RECORD_FIELD: lambda self: self.who_can_record,
    }

    def __str__(self):
        return f'{self.label} от {self.provider}'

    @property
    def notes(self):
        return ServiceNote.objects.filter(service=self)

    def have_permission(self, user, permission):
        check_function = self.PERMISSION_CHECKERS[
            self.PERMISSION_FIELDS_GETTERS[permission](self)
        ]
        return check_function(user, self)

    def process_permission(self, user, permission):
        if not self.have_permission(user, permission):
            raise PermissionDenied()

    def get_dates_with_notes(self):
        dates = set()
        for note in self.notes:
            dates.add(note.date)
        return dates

    def get_absolute_url(self):
        return reverse_lazy('one_service_calendar', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse_lazy('edit_service', kwargs={'pk': self.pk})

    def get_image_url(self):
        try:
            return self.image.url
        except ValueError:
            return ''


class ServiceNote(models.Model):
    provider = models.ForeignKey(User, on_delete=models.SET(-1), related_name='provider')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.SET(-1), blank=True, null=True, related_name='client')
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    provider_addition = models.CharField(max_length=255, blank=True, null=True)
    client_addition = models.CharField(max_length=255, blank=True, null=True)

    EMPTY = 0
    NEED_APPROVE = 1
    OCCUPIED = 2
    ENDED = 3
    STATUS_CHOICES = (
        (EMPTY, 'Свободно'),
        (NEED_APPROVE, 'Ожидает подтверждения'),
        (OCCUPIED, 'Занято'),
        (ENDED, 'Прошло'),
    )
    STATUS_CSS_CLASSES = (
        (EMPTY, 'success'),
        (NEED_APPROVE, 'info'),
        (OCCUPIED, 'warning'),
        (ENDED, 'secondary'),
    )
    status = models.IntegerField(default=EMPTY, choices=STATUS_CHOICES)

    def set_status(self, new_status):
        if self.date >= timezone.now().date():
            self.status = new_status
        else:
            self.status = self.ENDED
        self.save()

    @property
    def status_css(self):
        for status_pair in self.STATUS_CSS_CLASSES:
            if status_pair[0] == self.status:
                return status_pair[1]

    def is_free(self):
        return self.status == self.EMPTY

    def record(self, client, client_addition=None):
        self.service.process_permission(client, 'record')
        self.client_addition = client_addition
        if client == self.provider:
            self.set_status(self.OCCUPIED)
        else:
            if client.is_authenticated:
                self.client = client
            self.set_status(self.NEED_APPROVE)

    def is_need_approve(self):
        return self.status == self.NEED_APPROVE

    def approve(self, user):
        if user == self.provider:
            self.set_status(self.OCCUPIED)
        else:
            raise PermissionDenied()

    def can_be_canceled(self):
        return self.status in [self.OCCUPIED, self.NEED_APPROVE]

    def cancel(self, user):
        if user == self.provider or user == self.client:
            self.client = None
            self.client_addition = None
            self.set_status(self.EMPTY)
        else:
            raise PermissionDenied()

    def __str__(self):
        return f'{self.service} ' \
               f'{f" для {self.client}" if self.client is not None else ""} ' \
               f'на {self.date}, {self.time_start}-{self.time_end} ' \
               f'({self.get_status_display()})'

    def get_absolute_url(self):
        return reverse_lazy('one_service_day', kwargs={
            'pk': self.service.pk,
            'Y': self.date.year,
            'm': self.date.month,
            'd': self.date.day,
        })

    def get_delete_url(self):
        return reverse_lazy('delete_single_note', kwargs={
            'pk': self.pk,
        })

    def get_record_url(self):
        return reverse_lazy('record_to_note', kwargs={
            'pk': self.pk,
        })

    def get_approve_url(self):
        return reverse_lazy('approve_record_to_note', kwargs={
            'pk': self.pk,
        })

    def get_cancel_url(self):
        return reverse_lazy('cancel_record_to_note', kwargs={
            'pk': self.pk,
        })


class ServiceNoteGenerationPattern(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_time_start = models.TimeField()
    time_interval = models.TimeField()
    day_time_end = models.TimeField()
    multi_addition = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        string = f'С {self.day_time_start} до {self.day_time_end} с интервалом {self.time_interval}'
        if self.multi_addition is not None:
            string += f', примечание: {self.multi_addition}'
        return string

    def get_url(self, service: Service, date: datetime.date,
                postfix: str = 'execute'):
        return reverse_lazy(f'pattern_{postfix}', kwargs={
            'pk': service.pk,
            'Y': date.year,
            'm': date.month,
            'd': date.day,
            'pattern_pk': self.pk,
        })

    @staticmethod
    def get_timedelta_from_time(time: datetime.time):
        return datetime.timedelta(
            hours=time.hour, minutes=time.minute
        )

    @staticmethod
    def get_time_from_timedelta(timedelta: datetime.timedelta):
        return datetime.time(
            hour=timedelta.seconds // 3600,
            minute=timedelta.seconds % 3600 // 60
        )

    @staticmethod
    def create_single_note(service, date, start, end, addition=None):
        obj = ServiceNote(
            provider=service.provider, service=service, date=date,
            provider_addition=addition, time_start=start, time_end=end
        )
        obj.save()

    def generate_service_notes(self, service: Service, date: datetime.date):
        current = self.get_timedelta_from_time(self.day_time_start)
        interval = self.get_timedelta_from_time(self.time_interval)
        end = self.get_timedelta_from_time(self.day_time_end)
        addition = self.multi_addition
        while current < end:
            current_end = self.get_time_from_timedelta(current + interval)
            self.create_single_note(service, date,
                                    self.get_time_from_timedelta(current),
                                    current_end, addition)
            current = self.get_timedelta_from_time(current_end)


