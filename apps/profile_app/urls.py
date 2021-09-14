from django.urls import path
from settings.settings import ACTIVATION_REQUIRED

from django.contrib.auth import views as origin_auth_views
from apps.front_app.views import BaseDetailedView
from apps.profile_app import views as profile_views

urlpatterns = [
    path('<int:pk>/view/', profile_views.profile.ProfileView.as_view(), name='profile'),

    path('login/', profile_views.profile.LoginView.as_view(), name='login'),
    path('logout/', origin_auth_views.LogoutView.as_view(), name='logout'),

    path(
        '<int:pk>/password_change/',
        profile_views.change_password.PasswordChangeView.as_view(),
        name='password_change'
    ),

    path(
        'password_reset/',
        profile_views.change_password.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'reset/<uidb64>/<token>/',
        profile_views.change_password.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]

reg_patterns = [
    path(
        'register/closed/',
        BaseDetailedView.as_view(
            title='Регистрация закрыта',
            template_name='django_registration/registration_closed.html'
        ),
        name='django_registration_disallowed',
    ),
]

if not ACTIVATION_REQUIRED:
    reg_patterns += [
        path(
            'register/',
            profile_views.one_step_registration.RegistrationView.as_view(),
            name='register',
        ),
        path(
            'register/complete/',
            profile_views.one_step_registration.RegistrationCompleteView.as_view(),
            name='django_registration_complete',
        ),
    ]
else:
    reg_patterns += [
        path(
            'activate/complete/',
            profile_views.two_step_registration.ActivationCompleteView.as_view(),
            name='django_registration_activation_complete',
        ),
        path(
            'activate/<str:activation_key>/',
            profile_views.two_step_registration.ActivationView.as_view(),
            name='django_registration_activate',
        ),
        path(
            'register/',
            profile_views.two_step_registration.RegistrationView.as_view(),
            name='register',
        ),
        path(
            'register/complete/',
            profile_views.two_step_registration.RegistrationCompleteView.as_view(),
            name='django_registration_complete',
        ),
    ]

urlpatterns += reg_patterns
