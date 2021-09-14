from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django_registration.backends.one_step import \
    views as reg_one_step_views

from apps.front_app.views import BaseDetailedView
from apps.profile_app import forms as profile_forms, models as profile_models


class RegistrationView(reg_one_step_views.RegistrationView,
                       BaseDetailedView):
    title = 'Регистрация'
    template_name = 'django_registration/register.html'
    form_class = profile_forms.RegistrationFormUniqueEmail

    def register(self, form):
        new_user = super(RegistrationView, self).register(form)
        addition_info = profile_models.UserAdditionInfo(user=new_user)
        addition_info.save()
        return new_user


class RegistrationCompleteView(BaseDetailedView):
    def get(self, request, *args, **kwargs):
        self.add_message(
            f'Регистрация прошла успешно! '
            f'Теперь вам доступен весь функционал сайта',
            messages.SUCCESS
        )
        return HttpResponseRedirect(reverse_lazy('index'))
