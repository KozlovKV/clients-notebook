from django.shortcuts import render

from apps.front_app.views import BaseViewWithMenu


class ServicesListView(BaseViewWithMenu):
    template_name = 'services_list.html'


class OneServiceCalendarView(BaseViewWithMenu):
    template_name = 'one_service_calendar.html'


class OneServiceDayView(BaseViewWithMenu):
    template_name = 'one_service_day.html'
