from django.shortcuts import render

from apps.front_app.views import BaseViewWithMenu


class ServicesListView(BaseViewWithMenu):
    template_name = 'services_list.html'
