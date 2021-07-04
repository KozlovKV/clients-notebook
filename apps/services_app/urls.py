from django.urls import path

from apps.services_app import views as service_views

urlpatterns = [
    path('list/', service_views.ServicesListView.as_view(), name='services_list'),
    path('<int:pk>/', service_views.OneServiceCalendarView.as_view(), name='one_service_calendar'),
    path('<int:pk>/<int:Y>/<int:m>/<int:d>/', service_views.OneServiceDayView.as_view(), name='one_service_day'),
    path('my/list/', service_views.MyServicesListView.as_view(), name='my_services'),
    path('my/notes/', service_views.MyServiceNotesListView.as_view(), name='my_notes')
]