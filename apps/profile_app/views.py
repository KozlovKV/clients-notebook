from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages


from django.contrib.auth.models import User
import apps.profile_app.models as profile_models
from apps.services_app import models as service_models

from django.contrib.auth import views as auth_views
from django.views.generic import edit as generic_edit_views
from django_registration.backends.activation import views as reg_activation_views
from apps.front_app.views import BaseDetailedView

from apps.profile_app import forms as profile_forms


class LoginView(auth_views.LoginView, BaseDetailedView):
    template_name = 'auth/login_page.html'
    form_class = profile_forms.AuthForm


class RegistrationView(reg_activation_views.RegistrationView,
                       BaseDetailedView):
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

    def get(self, request, *args, **kwargs):
        resp = super(RegistrationView, self).get(request, *args, **kwargs)
        return resp


class RegistrationCompleteView(BaseDetailedView):
    def get(self, request, *args, **kwargs):
        self.add_message('Для заврешения регистрации подтвердите указанный при регистрации адерс электронной почты через высланное на него письмо', messages.INFO)
        return HttpResponseRedirect(reverse_lazy('index'))


class ActivationView(reg_activation_views.ActivationView, BaseDetailedView):
    success_url = reverse_lazy('django_activation_complete')


class PasswordChangeView(auth_views.PasswordChangeView, BaseDetailedView):
    form_class = profile_forms.PasswordChangeForm
    template_name = 'index.html'

    def get_success_url(self):
        self.add_message('Пароль успешно изменён', messages.SUCCESS)
        return reverse_lazy('profile', args=(self.request.user.pk, ))


class PasswordResetView(auth_views.PasswordResetView, BaseDetailedView):
    form_class = profile_forms.PasswordResetForm
    template_name = 'auth/password_reset_form.html'

    def get_success_url(self):
        self.add_message('Письмо отправлено', messages.INFO)
        return reverse_lazy('index')


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView, BaseDetailedView):
    form_class = profile_forms.SetPasswordForm
    template_name = 'auth/password_reset_confirm.html'

    def get_success_url(self):
        self.add_message('Пароль успешно изменён', messages.SUCCESS)
        return reverse_lazy('index')


class ProfileView(generic_edit_views.UpdateView, BaseDetailedView):
    object = None
    template_name = 'profile.html'
    model = User  # Using for getting url
    form_class = profile_forms.EditProfileForm

    def get_object(self, queryset=None):
        real_user = super(ProfileView, self).get_object(queryset)
        return profile_models.UserAdditionInfo.objects.get(user=real_user)

    def get_success_url(self):
        self.add_message('Данные успешно изменены', messages.SUCCESS)
        return super(ProfileView, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'object_list': service_models.Service.objects.filter(
                provider=self.object.user
            ),
            'change_password_form': profile_forms.PasswordChangeForm(
                user=self.request.user
            ),
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProfileView, self).get(request, *args, **kwargs)
