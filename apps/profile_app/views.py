from django.shortcuts import render
from django.contrib.auth import views as auth_views

from apps.front_app.views import BaseViewWithMenu
from apps.profile_app import forms as profile_forms


class LoginViewModified(auth_views.LoginView, BaseViewWithMenu):
    template_name = 'registration/register.html'
    form_class = profile_forms.AuthenticationFormModified
