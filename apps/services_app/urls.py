from django.urls import path

from apps.services_app import views as service_views

urlpatterns = [
    path('list/', service_views.ServicesListView.as_view(), name='services_list'),
    path(
        '<int:pk>/', service_views.OneServiceCalendarView.as_view(),
        name='one_service_calendar'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/',
        service_views.OneServiceDayView.as_view(), name='one_service_day'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/create/single/',
        service_views.CreateSingleServiceNoteView.as_view(),
        name='create_single_note'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/create/multi/',
        service_views.CreateMultiServiceNoteView.as_view(), name='create_multi_note'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/create/multi/pattern/<int:pattern_pk>/execute/',
        service_views.MultiServiceNoteExecutePatternView.as_view(),
        name='pattern_execute'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/create/multi/pattern/<int:pattern_pk>/edit/',
        service_views.MultiServiceNoteEditPatternView.as_view(),
        name='pattern_edit'
    ),
    path(
        'my/services/', service_views.MyServicesListView.as_view(),
        name='my_services'
    ),
    path(
        'my/services/create/', service_views.CreateServiceView.as_view(),
        name='create_service'
    ),
    path(
        'my/notes/', service_views.MyServiceNotesListView.as_view(),
        name='my_notes'
    ),
    path(
        'my/notes/delete/<int:pk>/',
        service_views.DeleteSingleServiceNoteView.as_view(),
        name='delete_single_note'
    ),
]