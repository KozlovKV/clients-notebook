from django.contrib import messages as messages
from django.http import HttpResponseRedirect
from django.views.generic import edit as generic_edit_views

from apps.front_app.views import BaseViewWithMenu
from apps.services_app import models as service_models, forms as service_forms
from apps.services_app.views.one_service import OneServiceDayView


class CreateSingleServiceNoteView(OneServiceDayView,
                                  generic_edit_views.CreateView):
    template_name = 'one_service_day.html'
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
        return super(CreateSingleServiceNoteView, self).form_valid(form)


class DeleteSingleServiceNoteView(BaseViewWithMenu,
                                  generic_edit_views.BaseDeleteView):
    template_name = 'my_notes.html'
    model = service_models.ServiceNote
    object = None

    def get_success_url(self):
        return self.object.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.request.user == self.object.service.provider:
            self.object.delete()
            self.add_message('Запись успешно удалена', messages.SUCCESS)
        else:
            self.add_message(
                'Вы не можете удалять записи, созданные другим пользователем',
                messages.ERROR
            )
        return HttpResponseRedirect(success_url)