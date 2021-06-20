from django.contrib.auth import forms as auth_forms
from django import forms


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
