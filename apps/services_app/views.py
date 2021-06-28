from django.shortcuts import render
from  django.views.generic import list as generic_list_views
from  django.views.generic import detail as generic_detail_views

from apps.front_app.views import BaseViewWithMenu

from apps.services_app import models as service_models


class ServicesListView(generic_list_views.ListView, BaseViewWithMenu):
    object_list = []
    model = service_models.Service
    template_name = 'services_list.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(ServicesListView, self).get(request, *args, **kwargs)


class OneServiceCalendarView(BaseViewWithMenu, generic_detail_views.DetailView):
    template_name = 'one_service_calendar.html'
    object = None
    model = service_models.Service

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(OneServiceCalendarView, self).get(request, *args, **kwargs)


class OneServiceDayView(BaseViewWithMenu):
    template_name = 'one_service_day.html'
