# forms.py

from django import forms
from django.utils import timezone
from .models import ScheduleMaintenance

class ScheduleMaintenanceForm(forms.ModelForm):
    class Meta:
        model = ScheduleMaintenance
        fields = ['content', 'time']
        labels = {
            'content': 'Maintenance Description',
            'time': 'Maintenance Time'
        }
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
    def clean_time(self):
        # Get the cleaned data for the time field
        time_value = self.cleaned_data['time']
        
        # Ensure that the datetime is timezone-aware
        if timezone.is_naive(time_value):
            # If the datetime is naive, make it timezone-aware using the current timezone
            time_value = timezone.make_aware(time_value, timezone=timezone.get_current_timezone())
        
        return time_value
class UpdateScheduleMaintenanceForm(forms.ModelForm):
    time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_time'})
    )
    content = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'id_content'})
    )
    status = forms.ChoiceField(
        choices=ScheduleMaintenance.STATUS_CHOICES,
        widget=forms.Select(attrs={'id': 'id_status'})
    )

    class Meta:
        model = ScheduleMaintenance
        fields = ['id', 'content', 'time', 'status']
        labels = {
            'id': 'Maintenance ID',
            'content': 'Maintenance Description',
            'time': 'Maintenance Time',
            'status': 'Status'
        }

        widgets = {
            # 'id': forms.TextInput(attrs={'id': 'maintenance_id'}),
            # 'time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_time','name':'id_time'}),
            # 'content': forms.TextInput(attrs={'id': 'id_content'}),
            # 'status': forms.Select(attrs={'id': 'id_status'}, choices=ScheduleMaintenance.STATUS_CHOICES)
        }
    def clean_time(self):
        # Get the cleaned data for the time field
        time_value = self.cleaned_data['time']
        
        # Ensure that the datetime is timezone-aware
        if timezone.is_naive(time_value):
            # If the datetime is naive, make it timezone-aware using the current timezone
            time_value = timezone.make_aware(time_value, timezone=timezone.get_current_timezone())
        
        return time_value