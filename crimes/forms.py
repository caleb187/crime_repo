from django import forms
from .models import Crime, Evidence

class CrimeReportForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = ['title', 'description', 'location', 'date_occurred', 'crime_type']
        widgets = {
            'date_occurred': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            })
        }

class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ['file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Describe the evidence...'
            })
        }

class CrimeAdminForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = [
            'title', 
            'description', 
            'crime_type', 
            'location', 
            'date_occurred', 
            'status',
            'priority'
        ]
        widgets = {
            'date_occurred': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'status-select'})
        self.fields['priority'].widget.attrs.update({'class': 'priority-select'})
