from django.urls import path
from django.contrib.auth import views as origin_auth_views
from apps.profile_app import views as profile_views

urlpatterns = [
    path('login/', profile_views.LoginViewModified.as_view(), name='login'),
    path('logout/', origin_auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/', origin_auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', origin_auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', origin_auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', origin_auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', origin_auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', origin_auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]