from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView
from django_registration.backends.activation import views as reg_activation_views

from apps.front_app.views import BaseViewWithMenu
from apps.profile_app import forms as profile_forms
from apps.profile_app.forms import EditProfileForm
from apps.profile_app.models import UserAdditionInfo


class LoginViewModified(auth_views.LoginView, BaseViewWithMenu):
    template_name = 'registration/register.html'
    form_class = profile_forms.AuthenticationFormModified


class RegistrationViewModified(reg_activation_views.RegistrationView, BaseViewWithMenu):
    email_subject_template = 'registration/activation_email_subject.txt'
    email_body_template = 'registration/activation_email_body.txt'
    template_name = 'registration/register.html'
    form_class = profile_forms.RegistrationFormUniqueEmailModified

    def register(self, form):
        new_user = super(RegistrationViewModified, self).register(form)
        addition_info = UserAdditionInfo(user=new_user)
        addition_info.save()
        return new_user

    def get_email_context(self, activation_key):
        context = super(RegistrationViewModified, self).get_email_context(activation_key)
        context.update({
            'activation_url': reverse_lazy('django_registration_activate', args=[activation_key, ]),
        })
        return context


class ActivationViewModified(reg_activation_views.ActivationView, BaseViewWithMenu):
    success_url = reverse_lazy('django_registration_complete')


class ProfileView(UpdateView, BaseViewWithMenu):
    object = None
    template_name = 'profile.html'
    model = UserAdditionInfo
    form_class = EditProfileForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProfileView, self).get(request, *args, **kwargs)