from django.urls import path

from django.contrib.auth import views as origin_auth_views
from apps.front_app.views import BaseDetailedView
from apps.profile_app import views as profile_views

urlpatterns = [
    path('<int:pk>/view/', profile_views.ProfileView.as_view(), name='profile'),

    path('login/', profile_views.LoginView.as_view(), name='login'),
    path('logout/', origin_auth_views.LogoutView.as_view(), name='logout'),

    path(
        '<int:pk>/password_change/',
        profile_views.PasswordChangeView.as_view(),
        name='password_change'
    ),

    path(
        'password_reset/',
        profile_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'reset/<uidb64>/<token>/',
        profile_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]

reg_patterns = [
    path(
        'activate/complete/',
        profile_views.ActivationCompleteView.as_view(),
        name='django_registration_activation_complete',
    ),
    path(
        'activate/<str:activation_key>/',
        profile_views.ActivationView.as_view(),
        name='django_registration_activate',
    ),
    path(
        'register/',
        profile_views.RegistrationView.as_view(),
        name='register',
    ),
    path(
        'register/complete/',
        profile_views.RegistrationCompleteView.as_view(),
        name='django_registration_complete',
    ),
    path(
        'register/closed/',
        BaseDetailedView.as_view(
            title='Регистрация закрыта',
            template_name='django_registration/registration_closed.html'
        ),
        name='django_registration_disallowed',
    ),
]

urlpatterns += reg_patterns
