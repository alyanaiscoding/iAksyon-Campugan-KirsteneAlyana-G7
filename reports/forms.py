
from django import forms
from .models import Report

class ReportPhotoWidget(forms.ClearableFileInput):
    template_name = "reports/widgets/photo_input.html"


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report

        fields = [
            "title",
            "description",
            "category",
            "location",
            "photo",
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
            "photo": ReportPhotoWidget(attrs={
                "accept": "image/*",
                "class": "photo-file-input",
            }),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")

        if photo:
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "Photo size must not exceed 5 MB."
                )

        return photo


class ReportStatusForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ["status"]
