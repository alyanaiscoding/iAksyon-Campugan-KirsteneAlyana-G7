from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from accounts.models import CustomUser
from .models import Report
from .forms import ReportForm


class ReportCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    CreateView
):
    model = Report
    form_class = ReportForm
    template_name = "reports/report_form.html"
    success_url = reverse_lazy("resident_dashboard")

    def test_func(self):
        return self.request.user.role == CustomUser.Role.RESIDENT

    def form_valid(self, form):
        form.instance.resident = self.request.user

        response = super().form_valid(form)

        messages.success(
            self.request,
            "Report submitted successfully!"
        )

        return response
    
class ReportListView(
LoginRequiredMixin,
UserPassesTestMixin,
ListView
):
    model = Report
    template_name = "reports/report_list.html"
    context_object_name = "reports"

    def test_func(self):
        return self.request.user.role == CustomUser.Role.RESIDENT

    def get_queryset(self):
        return Report.objects.filter(
            resident=self.request.user
        ).order_by("-created_at")