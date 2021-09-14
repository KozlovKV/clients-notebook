from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from apps.front_app.views import BaseDetailedView
from apps.profile_app import forms as profile_forms


class PasswordChangeView(auth_views.PasswordChangeView, BaseDetailedView):
    form_class = profile_forms.PasswordChangeForm
    template_name = 'index.html'

    def get_success_url(self):
        self.add_message('Пароль успешно изменён', messages.SUCCESS)
        return reverse_lazy('profile', args=(self.request.user.pk, ))


class PasswordResetView(auth_views.PasswordResetView, BaseDetailedView):
    title = 'Сброс пароля'
    form_class = profile_forms.PasswordResetForm
    template_name = 'auth/password_reset_form.html'

    def get_success_url(self):
        self.add_message('Письмо отправлено', messages.INFO)
        return reverse_lazy('index')


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView, BaseDetailedView):
    title = 'Создание нового пароля'
    post_reset_login = True
    form_class = profile_forms.SetPasswordForm
    template_name = 'auth/password_reset_confirm.html'

    def get_success_url(self):
        self.add_message('Пароль успешно изменён', messages.SUCCESS)
        return reverse_lazy('index')