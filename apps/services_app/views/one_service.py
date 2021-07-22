import datetime

from django.contrib import messages as messages
from django.urls import reverse_lazy
from django.views.generic import edit as generic_edit_views, \
    detail as generic_detail_views, list as generic_list_views

from apps.front_app.views import BaseViewWithMenu
from apps.services_app import models as service_models, forms as service_forms
from apps.services_app.views.lists import MyServicesListView, \
    MyServiceNotesListView


class CreateServiceView(MyServicesListView, generic_edit_views.BaseCreateView):
    template_name = 'my_services.html'
    object = None
    model = service_models.Service
    form_class = service_forms.ServiceForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.provider = self.request.user
        self.object.save()
        self.add_message('Услуга успешно создана', messages.SUCCESS)
        return super(CreateServiceView, self).form_valid(form)


class OneServiceCalendarView(BaseViewWithMenu, generic_detail_views.DetailView):
    template_name = 'one_service_calendar.html'
    object = None
    model = service_models.Service
    context_object_name = 'service'

    @staticmethod
    def get_dates_for_js(dates: list) -> list:
        js_dates = [date.isoformat() for date in dates]
        return js_dates

    def get_context_data(self, **kwargs):
        context = super(OneServiceCalendarView, self).get_context_data(**kwargs)
        context.update({
            'dates_with_notes': self.get_dates_for_js(
                self.object.get_dates_with_notes()
            ),
            'service_form': service_forms.ServiceForm(instance=self.object),
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(OneServiceCalendarView, self).get(request, *args, **kwargs)


class EditServiceView(OneServiceCalendarView,
                      generic_edit_views.BaseUpdateView):
    form_class = service_forms.ServiceForm


class DeleteServiceView(OneServiceCalendarView,
                        generic_edit_views.BaseDeleteView):
    def get_success_url(self):
        self.add_message('Услуга успешно удалена', messages.SUCCESS)
        return reverse_lazy('my_services')


class OneServiceDayView(BaseViewWithMenu, generic_list_views.ListView):
    template_name = 'one_service_day.html'
    object_list = []
    base_url_kwargs = {}

    @property
    def date(self):
        return datetime.date(self.kwargs['Y'], self.kwargs['m'],
                             self.kwargs['d'])

    @property
    def service(self):
        return service_models.Service.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        return MyServiceNotesListView.get_status_divided_notes_dicts(self.service.notes.filter(
            date=self.date
        ))

    def get_patterns(self):
        patterns_with_urls = []
        if self.request.user.is_authenticated:
            patterns_objects_list = service_models.ServiceNoteGenerationPattern.objects.filter(
                user=self.request.user)
            for pattern in patterns_objects_list:
                pattern_dict = {
                    'object': pattern,
                    'execute_url': pattern.get_url(self.service, self.date,
                                                   'execute'),
                    'edit_url': pattern.get_url(self.service, self.date,
                                                'edit'),
                }
                patterns_with_urls.append(pattern_dict)
        return patterns_with_urls

    def get_single_form_context(self):
        return {
            'single_form': service_forms.SingleServiceNoteForm(),
            'single_form_url': reverse_lazy('create_single_note',
                                            kwargs=self.base_url_kwargs),
        }

    def get_multi_form_context(self):
        return {
            'multi_form': service_forms.MultiServiceNoteForm(),
            'multi_form_url': reverse_lazy('create_multi_note',
                                           kwargs=self.base_url_kwargs),
            'multi_delete_url': reverse_lazy('delete_multi_note',
                                             kwargs=self.base_url_kwargs),
        }

    def get_context_data(self, **kwargs):
        context = super(OneServiceDayView, self).get_context_data(**kwargs)
        self.base_url_kwargs = {
            'pk': self.kwargs['pk'],
            'Y': self.kwargs['Y'],
            'm': self.kwargs['m'],
            'd': self.kwargs['d'],
        }
        context.update({
            'service': self.service,
            'date': self.date,
            'patterns': self.get_patterns(),
            'record_form': service_forms.RecordServiceNoteForm(),
        })
        context.update(self.get_single_form_context())
        context.update(self.get_multi_form_context())
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(OneServiceDayView, self).get(request, *args, **kwargs)
