from django.shortcuts import render
from  django.views.generic import list as list_views

from apps.front_app.views import BaseViewWithMenu

from apps.services_app import models as service_models


class ServicesListView(list_views.ListView, BaseViewWithMenu):
    object_list = []
    model = service_models.Service
    template_name = 'services_list.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(ServicesListView, self).get(request, *args, **kwargs)


class OneServiceCalendarView(BaseViewWithMenu):
    template_name = 'one_service_calendar.html'


class OneServiceDayView(BaseViewWithMenu):
    template_name = 'one_service_day.html'
