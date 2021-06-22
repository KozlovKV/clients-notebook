from typing import List

from django.urls import reverse
from django.views.generic import TemplateView

from apps.profile_app.forms import AuthenticationFormModified


class BaseViewWithMenu(TemplateView):
    @staticmethod
    def get_link_dict(url_name: str, human_name: str) -> dict:
        return {
            'url': reverse(url_name),
            'name': human_name,
        }

    def get_menu(self) -> List[dict]:
        return [
            self.get_link_dict('index', 'Главная'),
            self.get_link_dict('services_list', 'Запись на приём'),
            self.get_link_dict('index', 'Личный кабинет'),
            self.get_link_dict('index', 'Мои услуги'),
            self.get_link_dict('index', 'Мои записи'),
        ]

    def get_context_data(self, **kwargs):
        context = super(BaseViewWithMenu, self).get_context_data(**kwargs)
        context['menu'] = self.get_menu()
        context['login_form'] = AuthenticationFormModified()
        return context


class IndexView(BaseViewWithMenu):
    template_name = 'index.html'
