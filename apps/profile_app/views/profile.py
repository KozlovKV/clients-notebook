from django.contrib import messages

from django.contrib.auth.models import User
import apps.profile_app.models as profile_models
from apps.services_app import models as service_models

from django.contrib.auth import views as auth_views
from django.views.generic import edit as generic_edit_views
from apps.front_app.views import BaseDetailedView

from apps.profile_app import forms as profile_forms


class LoginView(auth_views.LoginView, BaseDetailedView):
    title = 'Вход'
    template_name = 'auth/login_page.html'
    form_class = profile_forms.AuthForm


class ProfileView(generic_edit_views.UpdateView, BaseDetailedView):
    object = None
    template_name = 'profile.html'
    model = User  # Using for getting url
    form_class = profile_forms.EditProfileForm

    def get_object(self, queryset=None):
        real_user = super(ProfileView, self).get_object(queryset)
        self.title = str(real_user)
        self.main_h1 = f'Профиль пользователя {self.title}'
        return profile_models.UserAdditionInfo.objects.get(user=real_user)

    def get_success_url(self):
        self.add_message('Данные успешно изменены', messages.SUCCESS)
        return super(ProfileView, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'services_list': service_models.Service.objects.filter(
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
