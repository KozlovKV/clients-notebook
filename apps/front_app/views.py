from typing import List

import requests
from django.urls import reverse
import django.contrib.messages as messages
from django.core.exceptions import PermissionDenied

from django.views.generic import TemplateView

import apps.profile_app.forms as profile_forms


class BaseDetailedView(TemplateView):
    THEME = 'Darkly'
    THEMES_JSON_URL = 'https://bootswatch.com/api/5.json'
    anons_allowed = True
    message_list = []

    @staticmethod
    def get_theme_css_url():
        json_request = requests.get(BaseDetailedView.THEMES_JSON_URL).json()
        for theme in json_request['themes']:
            if theme['name'] == BaseDetailedView.THEME:
                return theme['css']
        return ''

    @staticmethod
    def get_link_dict(url_name: str, human_name: str, kwargs: dict = {}) -> dict:
        return {
            'url': reverse(url_name, kwargs=kwargs),
            'name': human_name,
        }

    def get_menu(self) -> List[dict]:
        links = [
            self.get_link_dict('index', 'Главная'),
            self.get_link_dict('services_list', 'Запись на приём'),
        ]
        if self.request.user.is_authenticated:
            links += [
                self.get_link_dict(
                    'profile', f'Личный кабинет ({self.request.user})',
                    {'pk': self.request.user.pk}
                ),
                self.get_link_dict('my_services', 'Мои услуги'),
                self.get_link_dict('my_notes', 'Я записан'),
            ]
        return links

    def add_message(self, text, level=messages.INFO):
        messages.add_message(self.request, level, text)

    def get_context_data(self, **kwargs):
        context = super(BaseDetailedView, self).get_context_data(**kwargs)
        context.update({
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
    template_name = 'index.html'
