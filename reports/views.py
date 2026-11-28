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
from .forms import ReportForm, ReportStatusForm
from django.views.generic import UpdateView
from django.views.generic import DeleteView 
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404


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

class ReportUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Report
    form_class = ReportForm
    template_name = "reports/report_edit.html"
    success_url = reverse_lazy("report_list")

    def test_func(self):
        return self.request.user.role == CustomUser.Role.RESIDENT

    def get_queryset(self):
        return Report.objects.filter(
            resident=self.request.user,
            status=Report.Status.PENDING
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Report updated successfully!"
        )
        return response

class ReportDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Report
    template_name = "reports/report_confirm_delete.html"
    success_url = reverse_lazy("report_list")

    def test_func(self):
        return self.request.user.role == CustomUser.Role.RESIDENT

    def get_queryset(self):
        return Report.objects.filter(
            resident=self.request.user,
            status=Report.Status.PENDING
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Report deleted successfully!"
        )
        return response

class AdminReportListView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    ListView
):
    model = Report
    template_name = "reports/admin_report_list.html"
    context_object_name = "reports"

    def test_func(self):
        return self.request.user.role == CustomUser.Role.ADMIN

    def get_queryset(self):
        return Report.objects.select_related(
            "resident"
        ).order_by("-created_at")

class AdminReportUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Report
    form_class = ReportStatusForm
    template_name = "reports/admin_report_detail.html"
    success_url = reverse_lazy("admin_report_list")

    def test_func(self):
        return self.request.user.role == CustomUser.Role.ADMIN

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Report status updated successfully!"
        )
        return response

@login_required
def report_photo(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.user.role != "ADMIN" and report.resident_id != request.user.id:
        raise Http404("Photo not found.")

    if not report.photo:
        raise Http404("No photo attached.")

    try:
        return FileResponse(report.photo.open("rb"))
    except FileNotFoundError:
        raise Http404("Photo file not found.")