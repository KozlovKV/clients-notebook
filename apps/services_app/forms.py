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


class SingleServiceNoteForm(forms.ModelForm):
    class Meta:
        model = service_models.ServiceNote
        fields = [
            'time_start',
            'time_end',
            'addition',
        ]
        labels = {
            'time_start': 'Время начала',
            'time_end': 'Время конца',
            'addition': 'Дополнительная информация',
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
            'addition': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Дополнительная информация',
            }),
        }


class MultiServiceNoteForm(forms.Form):
    service = forms.Field(show_hidden_initial=True)
    date = forms.DateField(show_hidden_initial=True)
    day_time_start = forms.TimeField(
        label='Время начала дня *',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
    )
    time_interval = forms.TimeField(
        label='Интервал записи *',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
    )
    day_time_end = forms.TimeField(
        label='Время окончания дня *',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
    )
    multi_addition = forms.CharField(
        label='Дополнительная информация для всех карточек',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Дополнительная информация для всех карточек',
        })
    )
