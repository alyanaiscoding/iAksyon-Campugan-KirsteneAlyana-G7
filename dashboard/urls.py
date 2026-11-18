from django.urls import path
from .views import (
    DashboardView,
    AdminPanelView,
    ResidentDashboardView
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin-panel/", AdminPanelView.as_view(), name="admin_panel"),
    path("resident/", ResidentDashboardView.as_view(), name="resident_dashboard"),
]