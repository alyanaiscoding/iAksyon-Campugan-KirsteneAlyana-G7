from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re


class CustomeUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=150)
    last_name = forms.CharField(required=True, max_length=150)
    contact_number = forms.CharField(required=True, max_length=15)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "contact_number",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email address is already registered."
            )

        return email

    def clean_contact_number(self):
        contact_number = self.cleaned_data["contact_number"]

        if not re.fullmatch(r"09[0-9]{9}", contact_number):
            raise forms.ValidationError(
                "Enter a valid 11-digit mobile number starting with 09."
            )

        return contact_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.RESIDENT

        if commit:
            user.save()

        return user
        