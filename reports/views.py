
from zoneinfo import ZoneInfo
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncMonth
from accounts.models import CustomUser
from .models import Report
from .forms import ReportForm, ReportStatusForm


# RESIDENT - CREATE REPORT

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


# RESIDENT - VIEW REPORTS

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


# RESIDENT - UPDATE REPORT

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


# RESIDENT - DELETE REPORT

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


# ADMIN - VIEW ALL REPORTS

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


# ADMIN - UPDATE REPORT STATUS

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


# SECURE REPORT PHOTO ACCESS

@login_required
def report_photo(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if (
        request.user.role != CustomUser.Role.ADMIN
        and report.resident_id != request.user.id
    ):
        raise Http404("Photo not found.")

    if not report.photo:
        raise Http404("No photo attached.")

    try:
        return FileResponse(report.photo.open("rb"))

    except FileNotFoundError:
        raise Http404("Photo file not found.")


# ADMIN - ANALYTICS DASHBOARD

class AnalyticsDashboardView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    TemplateView
):
    template_name = "dashboard/analytics_dashboard.html"

    def test_func(self):
        return self.request.user.role == CustomUser.Role.ADMIN

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reports = Report.objects.all()

        # SUMMARY CARDS

        total = reports.count()

        pending = reports.filter(
            status=Report.Status.PENDING
        ).count()

        in_progress = reports.filter(
            status=Report.Status.IN_PROGRESS
        ).count()

        resolved = reports.filter(
            status=Report.Status.RESOLVED
        ).count()

        context["total_reports"] = total
        context["pending_reports"] = pending
        context["in_progress_reports"] = in_progress
        context["resolved_reports"] = resolved

        context["resolution_rate"] = (
            round((resolved / total) * 100, 2)
            if total > 0 else 0
        )

        # REPORTS BY CATEGORY

        category_counts = dict(
            reports.values("category")
            .annotate(count=Count("id"))
            .order_by("category")
            .values_list("category", "count")
        )

        context["category_labels"] = [
            label
            for value, label in Report.Category.choices
        ]

        context["category_counts"] = [
            category_counts.get(value, 0)
            for value, label in Report.Category.choices
        ]

        # REPORTS BY LOCATION

        location_data = list(
            reports.values("location")
            .annotate(count=Count("id"))
            .order_by("-count", "location")[:10]
        )

        context["location_labels"] = [
            item["location"]
            for item in location_data
        ]

        context["location_counts"] = [
            item["count"]
            for item in location_data
        ]

        # MONTHLY REPORT TRENDS

        monthly_data = list(
            reports.annotate(
                month=TruncMonth(
                    "created_at",
                    tzinfo=ZoneInfo("Asia/Manila")
                )
            )
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        monthly_counts = {
            item["month"].date(): item["count"]
            for item in monthly_data
        }

        monthly_labels = []
        monthly_values = []

        # Include months with zero reports

        if monthly_data:
            current = monthly_data[0]["month"].date()
            last = monthly_data[-1]["month"].date()

            while current <= last:
                monthly_labels.append(
                    current.strftime("%b %Y")
                )

                monthly_values.append(
                    monthly_counts.get(current, 0)
                )

                if current.month == 12:
                    current = current.replace(
                        year=current.year + 1,
                        month=1
                    )
                else:
                    current = current.replace(
                        month=current.month + 1
                    )

        context["monthly_labels"] = monthly_labels
        context["monthly_counts"] = monthly_values

        return context
