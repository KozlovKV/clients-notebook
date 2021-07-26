from itertools import chain

from django.urls import reverse_lazy
from django.views.generic import list as generic_list_views
from django.views.generic import edit as generic_edit_views

from apps.front_app.views import BaseDetailedView
from apps.services_app import models as service_models, forms as service_forms


class ServicesListView(BaseDetailedView, generic_list_views.BaseListView,
                       generic_edit_views.BaseFormView):
    template_name = 'services_list.html'
    object_list = []
    model = service_models.Service
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
        all_services = super(ServicesListView, self).get_queryset()
        return self.get_allowed_services(all_services)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(ServicesListView, self).get(request, *args, **kwargs)

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


class MyServicesListView(BaseDetailedView, generic_list_views.ListView):
    anons_allowed = False
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
        context.update({
            'object_list': self.get_queryset(),
        })
        context.update(self.get_service_form_context())
        return context

    def get(self, request, *args, **kwargs):
        return super(MyServicesListView, self).get(request, *args, **kwargs)


class MyServiceNotesListView(BaseDetailedView):
    anons_allowed = False
    template_name = 'my_notes.html'

    @staticmethod
    def get_status_divided_notes_dicts(notes):
        notes_dicts = []
        for status_id in range(len(service_models.ServiceNote.STATUS_CHOICES)):
            status_type_dict = {
                'name': service_models.ServiceNote.STATUS_CHOICES[status_id][1],
                'class':
                    service_models.ServiceNote.STATUS_CSS_CLASSES[status_id][1],
                'list': list(notes.filter(
                    status=
                    service_models.ServiceNote.STATUS_CSS_CLASSES[status_id][0]
                ))
            }
            status_type_dict['list'].sort(key=lambda x: (x.date, x.time_start))
            notes_dicts.append(status_type_dict)
        return notes_dicts

    def get_notes_me2other(self):
        notes = service_models.ServiceNote.objects.filter(
            client=self.request.user
        )
        return self.get_status_divided_notes_dicts(notes)

    def get_notes_other2me(self):
        notes = service_models.ServiceNote.objects.filter(
            provider=self.request.user
        )
        return self.get_status_divided_notes_dicts(notes)

    def get_context_data(self, **kwargs):
        context = super(MyServiceNotesListView, self).get_context_data(**kwargs)
        context.update({
            'object_list': self.get_notes_me2other(),
            'other2me': self.get_notes_other2me(),
        })
        return context
