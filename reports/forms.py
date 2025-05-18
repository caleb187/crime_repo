from django import forms
from .models import Report, ReportUpdate

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['crime', 'status', 'priority']
        widgets = {
            'priority': forms.NumberInput(attrs={'min': 0, 'max': 5}),
        }

class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = ReportUpdate
        fields = ['update_text']
        widgets = {
            'update_text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter update details...',
                'class': 'form-control'
            })
        }
