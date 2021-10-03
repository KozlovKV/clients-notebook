from django.http import HttpResponseRedirect

from django.views.generic import edit as generic_edit_views

from apps.services_app import models as service_models, forms as service_forms
from apps.services_app.views.multi_notes import MultiServiceNoteCreateView
from apps.services_app.views.one_service import OneServiceDayView


class MultiServiceNotePatternEditView(OneServiceDayView):
    anons_allowed = False

    def get_object(self):
        return service_models.ServiceNoteGenerationPattern.objects.get(
            pk=self.kwargs['pattern_pk']
        )

    def get_context_data(self, **kwargs):
        context = super(MultiServiceNotePatternEditView, self).get_context_data(
            **kwargs)
        context['multi_form'] = service_forms.MultiServiceNoteForm(
            instance=self.get_object()
        )
        return context


class MultiServiceNotePatternExecuteView(MultiServiceNotePatternEditView,
                                         MultiServiceNoteCreateView):
    anons_allowed = False

    def post(self, request, *args, **kwargs):
        pattern = self.get_object()
        form = service_forms.MultiServiceNoteForm(instance=pattern)
        self.form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class MultiServiceNotePatternDeleteView(generic_edit_views.BaseDeleteView, OneServiceDayView):
    anons_allowed = False
    model = service_models.ServiceNoteGenerationPattern
    pk_url_kwarg = 'pattern_pk'

    def get_success_url(self):
        self.add_message('Паттерн успешно удалён')
        return self.service.get_date_url(self.date)
