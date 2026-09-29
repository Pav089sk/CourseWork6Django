from django import forms
from .models import Messenger
from django.utils import timezone
from django.core.exceptions import ValidationError

class MessengerForm(forms.ModelForm):
    class Meta:
        model = Messenger
        fields = ['start_time', 'end_time', 'message', 'recipients']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time < timezone.now():
                raise ValidationError('Дата начала не может быть в прошлом.')
            if start_time >= end_time:
                raise ValidationError('Дата начала должна быть раньше даты окончания.')
        return cleaned_data
