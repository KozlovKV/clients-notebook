import datetime
from typing import List

from django.templatetags.static import static
from django.urls import reverse
import django.contrib.messages as messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from django.views.generic import TemplateView

import apps.profile_app.forms as profile_forms
from apps.services_app import models as service_models
from apps.services_app import sorter


class BaseDetailedView(TemplateView):
    class THEMES(enumerate):
        DEFAULT = 'bootstrap5/css/bootstrap.min.css'
        DARKLY = 'bootswatch-themes/darkly.css'
        CYBORG = 'bootswatch-themes/cyborg.css'

    title = ''
    main_h1 = None
    theme_url = THEMES.DARKLY
    anons_allowed = True
    message_list = []

    @staticmethod
    def get_link_dict(url_name: str, human_name: str, kwargs: dict = {}) -> dict:
        return {
            'url': reverse(url_name, kwargs=kwargs),
            'name': human_name,
        }

    def get_menu(self) -> List[dict]:
        links = [
            self.get_link_dict('index', 'Главная'),
            self.get_link_dict('services_list', 'Все услуги'),
        ]
        if self.request.user.is_authenticated:
            links += [
                self.get_link_dict(
                    'profile', f'Профиль ({self.request.user})',
                    {'pk': self.request.user.pk}
                ),
                self.get_link_dict('my_services', 'Мои услуги'),
                self.get_link_dict('me2other', 'Я записан'),
                self.get_link_dict('other2me', 'Ко мне записаны'),
            ]
        return links

    def get_theme_css_url(self):
        return static(self.theme_url)

    def add_message(self, text, level=messages.INFO):
        messages.add_message(self.request, level, text)

    def get_context_data(self, **kwargs):
        context = super(BaseDetailedView, self).get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'main_h1': self.main_h1,
            'theme_css_url': self.get_theme_css_url(),
            'menu': self.get_menu(),
            'login_form': profile_forms.AuthForm(),
            'messages': messages.get_messages(self.request),
        })
        return context

    def check_anons_allowing(self):
        if not (self.anons_allowed or self.request.user.is_authenticated):
            raise PermissionDenied()

    def get(self, request, *args, **kwargs):
        self.check_anons_allowing()
        return super(BaseDetailedView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_anons_allowing()
        return super(BaseDetailedView, self).post(request, *args, **kwargs)


class IndexView(BaseDetailedView):
    title = 'Главная'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = {}
        if self.request.user.is_authenticated:
            user = self.request.user
            self.main_h1 = f'Здравствуйте, {user.get_full_name()}!'
            context.update({
                'services_list': service_models.Service.objects.filter(
                    provider=user.pk
                ),
                'notes_list_today': sorter.ServiceNoteStatusSorter(
                    service_models.ServiceNote,
                    service_models.ServiceNote.objects.filter(
                        provider=user.pk, date=timezone.now().date()
                    )
                ).execute(),
                'notes_list_week': self.get_week_notes(),
            })
        context.update(super(IndexView, self).get_context_data(**kwargs))
        return context

    def get_week_notes(self):
        today = timezone.datetime.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = monday + datetime.timedelta(days=7)
        return sorter.ServiceNoteDateSorter(
            service_models.ServiceNote,
            service_models.ServiceNote.objects.filter(
                provider=self.request.user.pk,
                date__gte=monday, date__lte=sunday
            )
        ).execute()
