from django.urls import path

import apps.services_app.views as service_views


urlpatterns = [
    path(
        'list/', service_views.lists.ServicesListView.as_view(),
        name='services_list'),
    path(
        '<int:pk>/', service_views.one_service.OneServiceCalendarView.as_view(),
        name='one_service_calendar'
    ),
    path(
        '<int:pk>/edit/', service_views.one_service.EditServiceView.as_view(),
        name='edit_service'
    ),
    path(
        '<int:pk>/delete/', service_views.one_service.DeleteServiceView.as_view(),
        name='delete_service'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/',
        service_views.one_service.OneServiceDayView.as_view(),
        name='one_service_day'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/create/single/',
        service_views.one_note.SingleServiceNoteCreateView.as_view(),
        name='create_single_note'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/create/multi/',
        service_views.multi_notes.MultiServiceNoteCreateView.as_view(),
        name='create_multi_note'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/delete/multi/',
        service_views.multi_notes.MultiServiceNoteDeleteView.as_view(),
        name='delete_multi_note'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/create/multi/pattern/<int:pattern_pk>/execute/',
        service_views.multi_notes_pattern.MultiServiceNotePatternExecuteView.as_view(),
        name='pattern_execute'
    ),
    path(
        '<int:pk>/<int:Y>/<int:m>/<int:d>/create/multi/pattern/<int:pattern_pk>/edit/',
        service_views.multi_notes_pattern.MultiServiceNotePatternEditView.as_view(),
        name='pattern_edit'
    ),
    path(
        'my/services/', service_views.lists.MyServicesListView.as_view(),
        name='my_services'
    ),
    path(
        'my/services/create/', service_views.one_service.CreateServiceView.as_view(),
        name='create_service'
    ),
    path(
        'my/notes/me2other', service_views.lists.ServiceNotesWithMeListView.as_view(),
        name='me2other'
    ),
    path(
        'my/notes/other2me', service_views.lists.ServiceNotesToMeListView.as_view(),
        name='other2me'
    ),
    path(
        'my/notes/delete/<int:pk>/',
        service_views.one_note.SingleServiceNoteDeleteView.as_view(),
        name='delete_single_note'
    ),
    path(
        'my/notes/record/<int:pk>/',
        service_views.one_note.ServiceNoteRecordView.as_view(),
        name='record_to_note'
    ),
    path(
        'my/notes/approve/<int:pk>/',
        service_views.one_note.ServiceNoteApproveView.as_view(),
        name='approve_record_to_note'
    ),
    path(
        'my/notes/cancel/<int:pk>/',
        service_views.one_note.ServiceNoteCancelView.as_view(),
        name='cancel_record_to_note'
    ),
]