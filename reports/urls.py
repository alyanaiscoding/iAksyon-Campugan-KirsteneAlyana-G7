from django.urls import path
from .views import (
    ReportCreateView,
    ReportListView,
    ReportUpdateView
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
]