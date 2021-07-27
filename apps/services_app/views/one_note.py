from django.contrib import messages as messages
from django.http import HttpResponseRedirect
from django.views.generic import edit as generic_edit_views

from apps.front_app.views import BaseDetailedView
from apps.services_app import models as service_models, forms as service_forms
from apps.services_app.views.one_service import OneServiceDayView


class SingleServiceNoteCreateView(OneServiceDayView,
                                  generic_edit_views.CreateView):
    anons_allowed = False

    model = service_models.ServiceNote
    object = None
    form_class = service_forms.SingleServiceNoteForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.provider = self.service.provider
        self.object.service = self.service
        self.object.date = self.date
        self.object.save()
        self.add_message('Запись успешно создана', messages.SUCCESS)
        return super(SingleServiceNoteCreateView, self).form_valid(form)


class BaseServiceNoteEditView(BaseDetailedView,
                              generic_edit_views.BaseDetailView):
    template_name = 'index.html'
    model = service_models.ServiceNote
    object = None

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(self.get_success_url())


class ServiceNoteRecordView(BaseServiceNoteEditView,
                            generic_edit_views.BaseFormView):
    form_class = service_forms.RecordServiceNoteForm

    def form_valid(self, form):
        self.object.record(
            self.request.user, form.cleaned_data['client_addition']
        )
        if self.object.status == service_models.ServiceNote.OCCUPIED:
            self.add_message('Запись успешно произведена', messages.SUCCESS)
        else:
            self.add_message('Запись отправлена на одобрение поставщику',
                             messages.INFO)
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ServiceNoteApproveView(BaseServiceNoteEditView):
    anons_allowed = False

    def post(self, request, *args, **kwargs):
        resp = super(ServiceNoteApproveView, self).post(request, *args, **kwargs)
        self.object.approve(self.request.user)
        self.add_message('Запись успешно произведена', messages.SUCCESS)
        return resp


class ServiceNoteCancelView(BaseServiceNoteEditView):
    anons_allowed = False

    def post(self, request, *args, **kwargs):
        resp = super(ServiceNoteCancelView, self).post(request, *args, **kwargs)
        self.object.cancel(self.request.user)
        self.add_message('Запись успешно отменена', messages.SUCCESS)
        return resp


class SingleServiceNoteDeleteView(BaseServiceNoteEditView):
    anons_allowed = False

    def post(self, request, *args, **kwargs):
        resp = super(SingleServiceNoteDeleteView, self).post(request, *args, **kwargs)
        if self.request.user == self.object.provider:
            self.object.delete()
            self.add_message('Запись успешно удалена', messages.SUCCESS)
        else:
            self.add_message(
                'Вы не можете удалять записи, созданные другим пользователем',
                messages.ERROR
            )
        return resp
