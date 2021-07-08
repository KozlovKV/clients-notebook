import datetime
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.contrib import messages as messages

from django.views.generic import list as generic_list_views, FormView
from django.views.generic import detail as generic_detail_views
from django.views.generic import edit as generic_edit_views
from apps.front_app.views import BaseViewWithMenu

from apps.services_app import models as service_models

from apps.services_app import forms as service_forms


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


class CreateServiceView(MyServicesListView, generic_edit_views.BaseCreateView):
    template_name = 'my_services.html'
    object = None
    model = service_models.Service
    form_class = service_forms.ServiceForm
    success_url = reverse_lazy('my_services')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.provider = self.request.user
        self.object.save()
        self.add_message('Услуга успешно создана', messages.SUCCESS)
        return super(CreateServiceView, self).form_valid(form)


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
            'dates_with_notes': self.get_dates_for_js(
                self.object.get_dates_with_notes()
            ),
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
            'single_form': service_forms.SingleServiceNoteForm(),
            'single_form_url': reverse_lazy(
                'create_single_note', kwargs=self.kwargs
            ),
            'multi_form': service_forms.MultiServiceNoteForm(
                data={
                    'date': self.date,
                    'service': self.service,
                }
            ),
            'multi_form_url': reverse_lazy(
                'create_multi_note', kwargs=self.kwargs
            ),
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(OneServiceDayView, self).get(request, *args, **kwargs)


class CreateSingleServiceNote(OneServiceDayView, generic_edit_views.CreateView):
    template_name = 'one_service_day.html'
    model = service_models.ServiceNote
    object = None
    form_class = service_forms.SingleServiceNoteForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service = self.service
        self.object.date = self.date
        self.object.save()
        self.add_message('Запись успешно создана', messages.SUCCESS)
        return super(CreateSingleServiceNote, self).form_valid(form)


class CreateMultiServiceNote(OneServiceDayView, generic_edit_views.BaseFormView):
    template_name = 'one_service_day.html'
    form_class = service_forms.MultiServiceNoteForm

    def form_valid(self, form):
        self.service.generate_service_notes(self.date, form.cleaned_data)
        self.add_message('Записи успешно созданы', messages.SUCCESS)
        return super(CreateMultiServiceNote, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('one_service_day', kwargs=self.kwargs)
