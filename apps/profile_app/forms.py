from django.contrib.auth.models import User
import apps.profile_app.models as profile_models

from django import forms
from django.contrib.auth import forms as auth_forms, password_validation
from django_registration import forms as reg_forms

from django.utils.translation import gettext_lazy as _


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = profile_models.UserAdditionInfo
        fields = ['avatar', 'about']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control-lg w-100',
            }),
            'about': forms.TextInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Кратко расскажите о себе, своих навыках',
            })
        }
        labels = {
            'avatar': 'Аватарка',
            'about': 'О себе',
        }


class AuthForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control w-100',
                'placeholder': 'Имя пользователя',
            }
        )
    )
    password = forms.CharField(
        strip=False, label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': 'form-control w-100',
                'placeholder': 'Пароль',
            }
        ),
    )


class SetPasswordForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control-lg w-100',
            'placeholder': _('New password'),
            'autocomplete': 'new-password',
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control-lg w-100',
            'placeholder': _('New password confirmation'),
            'autocomplete': 'new-password',
        }),
    )


class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(
        label=_('Old password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control-lg w-100',
            'placeholder': _('Old password'),
            'autocomplete': 'current-password',
            'autofocus': True
        }),
    )


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control-lg w-100',
            'placeholder': _('Email'),
            'autocomplete': 'email',
        })
    )


class RegistrationFormUniqueEmail(reg_forms.RegistrationFormUniqueEmail):
    class Meta(reg_forms.RegistrationFormUniqueEmail.Meta):
        fields = [
            'first_name',
            'last_name',
            User.USERNAME_FIELD,
            User.get_email_field_name(),
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Имя',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Фамилия',
            }),
            User.USERNAME_FIELD: forms.TextInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Имя пользователя',
            }),
            User.get_email_field_name(): forms.EmailInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Электронная почта',
            }),
        }

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            User.USERNAME_FIELD: 'Имя пользователя',
            User.get_email_field_name(): 'Электронная почта',
        }

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Пароль',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=forms.PasswordInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Повторите пароль',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
