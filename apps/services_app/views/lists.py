from itertools import chain

from django.urls import reverse_lazy
from django.views.generic import list as generic_list_views
from django.views.generic import edit as generic_edit_views

from apps.front_app.views import BaseDetailedView
from apps.services_app import models as service_models, forms as service_forms
from apps.services_app import sorter


class ServicesListView(generic_list_views.BaseListView, BaseDetailedView,
                       generic_edit_views.BaseFormView):
    title = 'Список услуг'
    template_name = 'services_list.html'
    object_list = []
    model = service_models.Service
    context_object_name = 'services_list'
    form_class = service_forms.ServiceSearchForm
    success_url = reverse_lazy('services_list')

    def get_allowed_services(self, all_services):
        if not self.request.user.is_authenticated:
            return all_services.filter(who_can_see=self.model.ALL)
        return chain(
            all_services.exclude(who_can_see=self.model.ONLY_PROVIDER),
            all_services.filter(
                who_can_see=self.model.ONLY_PROVIDER,
                provider=self.request.user
            )
        )

    def get_queryset(self):
        all_services = super(ServicesListView, self).get_queryset().select_related('provider')
        return self.get_allowed_services(all_services)

    def form_valid(self, form):
        data = form.cleaned_data
        self.object_list = self.model.objects.filter(
            label__icontains=data.get('label', ''),
            description__icontains=data.get('description', ''),
        )
        self.object_list = self.get_allowed_services(self.object_list)
        self.add_message(f'Найдено совпадений: {len(self.object_list)}')
        context = self.get_context_data(**self.kwargs)
        return self.render_to_response(context, **self.kwargs)


class MyServicesListView(generic_list_views.BaseListView, BaseDetailedView):
    title = 'Мои услуги'
    anons_allowed = False
    template_name = 'my_services.html'
    object_list = []
    model = service_models.Service
    context_object_name = 'services_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(provider=self.request.user)
        return []

    def get_service_form_context(self):
        return {
            'service_form': service_forms.ServiceForm(data={
                'provider': self.request.user,
            }),
            'service_form_url': reverse_lazy('create_service'),
            'service_form_submit_value': 'Создать',
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_service_form_context())
        return context


class ServiceNotesWithMeListView(generic_list_views.BaseListView, BaseDetailedView):
    title = 'Я записан'
    anons_allowed = False
    template_name = 'my_notes.html'
    model = service_models.ServiceNote
    object_list = []
    context_object_name = 'notes_list_l2'

    def get_raw_notes(self):
        return self.model.objects.filter(client=self.request.user).select_related('service', 'provider', 'client')

    def get_queryset(self):
        notes = self.get_raw_notes()
        dicts_list = sorter.ServiceNoteDateSorter(
            service_models.ServiceNote, notes
        ).execute()
        for dict_l1 in dicts_list:
            dict_l1['list'] = sorter.ServiceNoteStatusSorter(
                service_models.ServiceNote, dict_l1['list']
            ).execute(dict_l1['id'])
        return dicts_list


class ServiceNotesToMeListView(ServiceNotesWithMeListView):
    title = 'Ко мне записаны'

    def get_raw_notes(self):
        return self.model.objects.filter(provider=self.request.user).select_related('service', 'provider', 'client')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ServiceNotesToMeListView, self).get_context_data(object_list=None, **kwargs)
        return context
