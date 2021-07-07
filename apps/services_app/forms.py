from django.forms import fields
from apps.services_app import models as service_models

from django import forms


class ServiceForm(forms.ModelForm):
    class Meta:
        model = service_models.Service
        fields = [
            'label',
            'image',
            'description',
        ]
        labels = {
            'label': 'Название',
            'image': 'Изображение',
            'description': 'Описание',
        }
        widgets = {
            'label': forms.TextInput(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Название',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-lg w-100',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control-lg w-100',
                'placeholder': 'Описание',
            }),
        }