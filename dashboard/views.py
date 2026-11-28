
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.db.models import Count, Q

from accounts.models import CustomUser
from reports.models import Report


class AdminPanelView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    TemplateView
):
    template_name = "dashboard/admin_panel.html"

    def test_func(self):
        return self.request.user.role == CustomUser.Role.ADMIN


class ResidentDashboardView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    TemplateView
):
    template_name = "dashboard/resident_dashboard.html"

    def test_func(self):
        return self.request.user.role == CustomUser.Role.RESIDENT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get reports belonging to the logged-in resident only
        reports = Report.objects.filter(
            resident=self.request.user
        )

        # Report statistics
        statistics = reports.aggregate(
            total_reports=Count("id"),

            pending_reports=Count(
                "id",
                filter=Q(status=Report.Status.PENDING)
            ),

            in_progress_reports=Count(
                "id",
                filter=Q(status=Report.Status.IN_PROGRESS)
            ),

            resolved_reports=Count(
                "id",
                filter=Q(status=Report.Status.RESOLVED)
            )
        )

        context.update(statistics)

        # Three most recent reports
        context["recent_reports"] = reports.order_by(
            "-created_at"
        )[:3]

        # Resolution rate
        total = statistics["total_reports"]
        resolved = statistics["resolved_reports"]

        context["resolution_rate"] = (
            round((resolved / total) * 100)
            if total > 0 else 0
        )

        return context


class DashboardView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.role == CustomUser.Role.ADMIN:
            return redirect("admin_panel")

        return redirect("resident_dashboard")
