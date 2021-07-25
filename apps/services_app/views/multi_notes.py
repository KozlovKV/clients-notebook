from django.contrib import messages as messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import edit as generic_edit_views

from apps.services_app import forms as service_forms
from apps.services_app.views.one_service import OneServiceDayView


class MultiServiceNoteCreateView(OneServiceDayView,
                                 generic_edit_views.BaseFormView):
    anons_allowed = False
    template_name = 'one_service_day.html'
    form_class = service_forms.MultiServiceNoteForm

    def form_valid(self, form):
        pattern = form.save(commit=False)
        if form.data.get('save', False):
            pattern.user = self.request.user
            pattern.save()
        pattern.generate_service_notes(self.service, self.date)
        self.add_message('Записи успешно созданы', messages.SUCCESS)
        return super(MultiServiceNoteCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('one_service_day', args=(
            self.kwargs['pk'], self.kwargs['Y'],
            self.kwargs['m'], self.kwargs['d'],
        ))


class MultiServiceNoteDeleteView(OneServiceDayView):
    anons_allowed = False
    template_name = 'one_service_day.html'

    def delete(self, request, *args, **kwargs):
        self.object_list = self.get_notes_list()
        success_url = self.get_success_url()
        if len(self.object_list) > 0:
            if self.request.user == self.object_list[0].provider:
                self.object_list.delete()
                self.add_message('Записи успешно удалены', messages.SUCCESS)
            else:
                self.add_message(
                    'Вы не можете удалять записи, созданные другим пользователем',
                    messages.ERROR
                )
        else:
            self.add_message(
                'Для данной услуги нет записей на эту дату',
                messages.ERROR
            )
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy('one_service_day', args=(
            self.kwargs['pk'], self.kwargs['Y'],
            self.kwargs['m'], self.kwargs['d'],
        ))

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)