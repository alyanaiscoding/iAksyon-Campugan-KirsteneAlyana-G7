from django.urls import path
from .views import (
    ReportCreateView,
    ReportListView,
    ReportUpdateView,
    ReportDeleteView,
    AdminReportListView,
    AdminReportUpdateView
)

urlpatterns = [
    path(
        "create/",
        ReportCreateView.as_view(),
        name="report_create"
    ),
    path(
        "my-reports/",
        ReportListView.as_view(),
        name="report_list"
    ),
    path(
        "<int:pk>/edit/",
        ReportUpdateView.as_view(),
        name="report_update"
    ),
    path(
        "<int:pk>/delete/",
        ReportDeleteView.as_view(),
        name="report_delete"
    ),
    path(
        "manage/",
        AdminReportListView.as_view(),
        name="admin_report_list"
    ),
    path(
        "manage/<int:pk>/",
        AdminReportUpdateView.as_view(),
        name="admin_report_update"
    ),
]