from django.urls import path

from apps.services_app import views as service

urlpatterns = [
    path('list/', service.ServicesListView.as_view(), name='services_list'),
    path('<int:pk>/', service.OneServiceCalendarView.as_view(), name='one_service_calendar'),
    path('<int:pk>/<int:Y>/<int:m>/<int:d>/', service.OneServiceDayView.as_view(), name='one_service_day'),
    path('my/list/', service.MyServicesListView.as_view(), name='my_services'),
]