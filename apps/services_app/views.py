import datetime

from django.shortcuts import render
from  django.views.generic import list as generic_list_views
from  django.views.generic import detail as generic_detail_views

from apps.front_app.views import BaseViewWithMenu

from apps.services_app import models as service_models


class ServicesListView(BaseViewWithMenu, generic_list_views.ListView):
    template_name = 'services_list.html'
    object_list = []
    model = service_models.Service

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(ServicesListView, self).get(request, *args, **kwargs)


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
