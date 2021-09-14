from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django_registration.backends.activation import \
    views as reg_activation_views

from apps.front_app.views import BaseDetailedView
from apps.profile_app import forms as profile_forms, models as profile_models


class RegistrationView(reg_activation_views.RegistrationView,
                       BaseDetailedView):
    title = 'Регистрация'
    email_subject_template = 'django_registration/activation_email_subject.txt'
    email_body_template = 'django_registration/activation_email_body.txt'
    template_name = 'django_registration/register.html'
    form_class = profile_forms.RegistrationFormUniqueEmail

    def register(self, form):
        new_user = super(RegistrationView, self).register(form)
        addition_info = profile_models.UserAdditionInfo(user=new_user)
        addition_info.save()
        return new_user

    def get_email_context(self, activation_key):
        context = super(RegistrationView, self).get_email_context(
            activation_key
        )
        context.update({
            'activation_url': reverse_lazy(
                'django_registration_activate',
                args=[activation_key, ]
            ),
        })
        return context


class RegistrationCompleteView(BaseDetailedView):
    def get(self, request, *args, **kwargs):
        self.add_message(
            f'Для завершения регистрации подтвердите указанный при регистрации '
            f'адрес электронной почты через высланное на него письмо',
            messages.INFO)
        return HttpResponseRedirect(reverse_lazy('index'))


class ActivationView(reg_activation_views.ActivationView, BaseDetailedView):
    title = 'Активация аккаунта'

    def activate(self, *args, **kwargs):
        user = super(ActivationView, self).activate(*args, **kwargs)
        login(self.request, user)
        return user


class ActivationCompleteView(BaseDetailedView):
    def get(self, request, *args, **kwargs):
        self.add_message(
            f'Ваш аккаунт активирован! '
            f'Теперь вам доступен весь функционал сайта',
            messages.SUCCESS)
        return HttpResponseRedirect(reverse_lazy('index'))