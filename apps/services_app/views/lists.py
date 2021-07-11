from django.urls import reverse_lazy
from django.views.generic import list as generic_list_views

from apps.front_app.views import BaseViewWithMenu
from apps.services_app import models as service_models, forms as service_forms


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
    form_class = service_forms.ServiceForm
    success_url = reverse_lazy('my_services')

    def get_queryset(self):
        queryset = []
        if self.request.user.is_authenticated:
            queryset = service_models.Service.objects.filter(
                provider=self.request.user
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_list': self.get_queryset(),
            'service_form': service_forms.ServiceForm(data={
                'provider': self.request.user,
            }),
        })
        return context

    def get(self, request, *args, **kwargs):
        return super(MyServicesListView, self).get(request, *args, **kwargs)


class MyServiceNotesListView(BaseViewWithMenu):
    template_name = 'my_notes.html'

    def get_notes_me2other(self):
        return service_models.ServiceNote.objects.filter(
            client=self.request.user)

    def get_notes_other2me(self):
        my_services = service_models.Service.objects.filter(
            provider=self.request.user)
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
