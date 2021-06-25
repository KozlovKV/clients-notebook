from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django_registration.backends.activation import views as reg_activation_views

from apps.front_app.views import BaseViewWithMenu
from apps.profile_app import forms as profile_forms


class LoginViewModified(auth_views.LoginView, BaseViewWithMenu):
    template_name = 'registration/register.html'
    form_class = profile_forms.AuthenticationFormModified


class RegistrationViewModified(reg_activation_views.RegistrationView, BaseViewWithMenu):
    email_subject_template = 'registration/activation_email_subject.txt'
    email_body_template = 'registration/activation_email_body.txt'
    template_name = 'registration/register.html'
    form_class = profile_forms.RegistrationFormUniqueEmailModified

    def get_email_context(self, activation_key):
        context = super(RegistrationViewModified, self).get_email_context(activation_key)
        context.update({
            'activation_url': reverse_lazy('django_registration_activate', args=[activation_key, ]),
        })
        return context


class ActivationViewModified(reg_activation_views.ActivationView, BaseViewWithMenu):
    success_url = reverse_lazy('django_registration_complete')


class ProfileView(BaseViewWithMenu):
    template_name = 'profile.html'
