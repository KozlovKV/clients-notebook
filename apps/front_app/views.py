from typing import List

from django.urls import reverse
import django.contrib.messages as messages

from django.views.generic import TemplateView

import apps.profile_app.forms as profile_forms


class BaseViewWithMenu(TemplateView):
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
            self.get_link_dict('services_list', 'Запись на приём'),
        ]
        if self.request.user.is_authenticated:
            links += [
                self.get_link_dict(
                    'profile', f'Личный кабинет ({self.request.user})',
                    {'pk': self.request.user.pk}
                ),
                self.get_link_dict('my_services', 'Мои услуги'),
                self.get_link_dict('my_notes', 'Мои записи'),
            ]
        return links

    def add_message(self, text, level=messages.INFO):
        messages.add_message(self.request, level, text)

    def get_context_data(self, **kwargs):
        context = super(BaseViewWithMenu, self).get_context_data(**kwargs)
        context['menu'] = self.get_menu()
        context['login_form'] = profile_forms.AuthenticationFormModified()
        context['messages'] = messages.get_messages(self.request)
        return context


class IndexView(BaseViewWithMenu):
    template_name = 'index.html'
