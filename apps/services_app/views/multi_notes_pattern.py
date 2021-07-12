from apps.services_app import models as service_models, forms as service_forms
from apps.services_app.views.multi_notes import CreateMultiServiceNoteView
from apps.services_app.views.one_service import OneServiceDayView


class MultiServiceNoteEditPatternView(OneServiceDayView):
    def get_object(self):
        return service_models.ServiceNoteGenerationPattern.objects.get(
            pk=self.kwargs['pattern_pk']
        )

    def get_context_data(self, **kwargs):
        context = super(MultiServiceNoteEditPatternView, self).get_context_data(
            **kwargs)
        context['multi_form'] = service_forms.MultiServiceNoteForm(
            instance=self.get_object()
        )
        return context


class MultiServiceNoteExecutePatternView(MultiServiceNoteEditPatternView,
                                         CreateMultiServiceNoteView):
    def get(self, request, *args, **kwargs):
        response = super(MultiServiceNoteExecutePatternView, self).get(request,
                                                                       *args,
                                                                       **kwargs)
        pattern = self.get_object()
        form = service_forms.MultiServiceNoteForm(instance=pattern)
        self.form_valid(form)
        return response
