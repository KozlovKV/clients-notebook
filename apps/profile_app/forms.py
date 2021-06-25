from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django_registration import forms as reg_forms
from django import forms

from apps.profile_app.models import UserAdditionInfo


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserAdditionInfo
        fields = ['avatar', 'about']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'about': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кратко расскажите о себе, своих навыках',
            })
        }
        labels = {
            'avatar': 'Аватарка',
            'about': 'О себе',
        }


class AuthenticationFormModified(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control m-1 col',
                'placeholder': 'Имя пользователя',
            }
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': 'form-control m-1 col',
                'placeholder': 'Пароль',
            }
        ),
    )


class RegistrationFormUniqueEmailModified(reg_forms.RegistrationFormUniqueEmail):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            'password1',
            'password2',
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
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Пароль',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Повторите пароль',
            }),
        }

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            User.USERNAME_FIELD: 'Имя пользователя',
            User.get_email_field_name(): 'Электронная почта',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
