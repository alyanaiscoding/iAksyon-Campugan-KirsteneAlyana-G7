from django.urls import path
from .views import ReportCreateView, ReportListView


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
]