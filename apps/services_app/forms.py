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
                'rows': 2,
                'class': 'form-control-lg w-100',
                'placeholder': 'Описание',
            }),
        }


class ServiceSearchForm(forms.Form):
    label = forms.CharField(
        label='Название', required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-lg w-100',
            'placeholder': 'Название',
        })
    )
    description = forms.CharField(
        label='Описание', required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-lg w-100',
            'placeholder': 'Описание',
        })
    )


class SingleServiceNoteForm(forms.ModelForm):
    class Meta:
        model = service_models.ServiceNote
        fields = [
            'time_start',
            'time_end',
            'provider_addition',
        ]
        labels = {
            'time_start': 'Время начала',
            'time_end': 'Время конца',
            'provider_addition': 'Дополнительная информация',
        }
        widgets = {
            'time_start': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'time_end': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'provider_addition': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Дополнительная информация',
            }),
        }


class MultiServiceNoteForm(forms.ModelForm):
    class Meta:
        model = service_models.ServiceNoteGenerationPattern
        fields = [
            'day_time_start',
            'time_interval',
            'day_time_end',
            'multi_addition',
        ]
        labels = {
            'day_time_start': 'Время начала дня *',
            'time_interval': 'Интервал записи *',
            'day_time_end': 'Время окончания дня *',
            'multi_addition': 'Дополнительная информация для всех карточек',
        }
        widgets = {
            'day_time_start': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'time_interval': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'day_time_end': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'multi_addition': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Дополнительная информация для всех карточек',
            }),
        }


class RecordServiceNoteForm(forms.ModelForm):
    class Meta:
        model = service_models.ServiceNote
        fields = [
            'client_addition'
        ]
        widgets = {
            'client_addition': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дополнительная информация',
            })
        }
