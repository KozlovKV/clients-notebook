from django.contrib import admin
import apps.services_app.models as services_models


admin.site.register(services_models.Service)
admin.site.register(services_models.ServiceNote)
admin.site.register(services_models.ServiceNoteGenerationPattern)
