from django.urls import path
from .views import (
    ReportCreateView,
    ReportListView,
    ReportUpdateView,
    ReportDeleteView
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
]