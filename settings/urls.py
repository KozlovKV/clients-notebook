"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.front_app import views as front
from apps.services_app import views as service

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', front.IndexView.as_view(), name='index'),
    path('service/', service.ServicesListView.as_view(), name='services_list'),
    path('service/<int:id>/', service.OneServiceView.as_view(), name='one_service'),
]
