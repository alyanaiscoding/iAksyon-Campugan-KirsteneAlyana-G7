from django import forms
from .models import Report


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report

        fields = [
            "title",
            "description",
            "category",
            "location",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Enter report title"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Describe the community issue",
                "rows": 5
            }),
            "location": forms.TextInput(attrs={
                "placeholder": "Enter the location of the issue"
            }),
        }

class ReportStatusForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["status"]