from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import TemplateView
from django.shortcuts import redirect
from accounts.models import CustomUser


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


class DashboardView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.role == CustomUser.Role.ADMIN:
            return redirect("admin_panel")

        return redirect("resident_dashboard")