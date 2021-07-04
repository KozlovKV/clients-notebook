import datetime

from django.views.generic import list as generic_list_views
from django.views.generic import detail as generic_detail_views
from apps.front_app.views import BaseViewWithMenu

from apps.services_app import models as service_models


class ServicesListView(BaseViewWithMenu, generic_list_views.ListView):
    template_name = 'services_list.html'
    object_list = []
    model = service_models.Service

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(ServicesListView, self).get(request, *args, **kwargs)


class MyServicesListView(BaseViewWithMenu, generic_list_views.ListView):
    template_name = 'my_services.html'
    object_list = []
    model = service_models.Service

    def get_queryset(self):
        queryset = super(MyServicesListView, self).get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(provider=self.request.user)
        else:
            return []

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(MyServicesListView, self).get(request, *args, **kwargs)


class MyServiceNotesListView(BaseViewWithMenu):
    template_name = 'my_notes.html'

    def get_notes_me2other(self):
        return service_models.ServiceNote.objects.filter(client=self.request.user)

    def get_notes_other2me(self):
        my_services = service_models.Service.objects.filter(provider=self.request.user)
        notes = []
        for service in my_services:
            notes += service_models.ServiceNote.objects.filter(service=service)
        return notes

    def get_context_data(self, **kwargs):
        context = super(MyServiceNotesListView, self).get_context_data(**kwargs)
        context.update({
            'me2other': self.get_notes_me2other(),
            'other2me': self.get_notes_other2me(),
        })
        return context


class OneServiceCalendarView(BaseViewWithMenu, generic_detail_views.DetailView):
    template_name = 'one_service_calendar.html'
    object = None
    model = service_models.Service

    @staticmethod
    def get_dates_for_js(dates: list) -> list:
        js_dates = [date.isoformat() for date in dates]
        return js_dates

    def get_context_data(self, **kwargs):
        context = super(OneServiceCalendarView, self).get_context_data(**kwargs)
        context.update({
            'dates_with_notes': self.get_dates_for_js(self.object.get_dates_with_notes()),
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(OneServiceCalendarView, self).get(request, *args, **kwargs)


class OneServiceDayView(BaseViewWithMenu, generic_list_views.ListView):
    template_name = 'one_service_day.html'
    object_list = []
    model = service_models.ServiceNote

    @property
    def date(self):
        return datetime.date(self.kwargs['Y'], self.kwargs['m'], self.kwargs['d'])

    @property
    def service(self):
        return service_models.Service.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.service.get_notes_by_date(self.date)

    def get_context_data(self, **kwargs):
        context = super(OneServiceDayView, self).get_context_data(**kwargs)
        context.update({
            'service': self.service,
            'date': self.date,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(OneServiceDayView, self).get(request, *args, **kwargs)
