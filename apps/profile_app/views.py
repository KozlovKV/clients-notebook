from django.urls import reverse_lazy
from django.contrib import messages


from django.contrib.auth.models import User
import apps.profile_app.models as profile_models

from django.contrib.auth import views as auth_views
from django.views.generic import edit as generic_edit_views
from django_registration.backends.activation import views as reg_activation_views
from apps.front_app.views import BaseViewWithMenu

from apps.profile_app import forms as profile_forms


class LoginViewModified(auth_views.LoginView, BaseViewWithMenu):
    template_name = 'auth/login_page.html'
    form_class = profile_forms.AuthenticationFormModified


class RegistrationViewModified(reg_activation_views.RegistrationView, BaseViewWithMenu):
    email_subject_template = 'registration/activation_email_subject.txt'
    email_body_template = 'registration/activation_email_body.txt'
    template_name = 'registration/register.html'
    form_class = profile_forms.RegistrationFormUniqueEmailModified

    def register(self, form):
        new_user = super(RegistrationViewModified, self).register(form)
        addition_info = profile_models.UserAdditionInfo(user=new_user)
        addition_info.save()
        return new_user

    def get_email_context(self, activation_key):
        context = super(RegistrationViewModified, self).get_email_context(activation_key)
        context.update({
            'activation_url': reverse_lazy('django_registration_activate', args=[activation_key, ]),
        })
        return context

    def get(self, request, *args, **kwargs):
        resp = super(RegistrationViewModified, self).get(request, *args, **kwargs)
        return resp


class ActivationViewModified(reg_activation_views.ActivationView, BaseViewWithMenu):
    success_url = reverse_lazy('django_registration_complete')


class ProfileView(generic_edit_views.UpdateView, BaseViewWithMenu):
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProfileView, self).get(request, *args, **kwargs)
