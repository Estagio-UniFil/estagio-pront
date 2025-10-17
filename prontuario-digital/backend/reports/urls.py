from django.urls import path
from reports import views

urlpatterns = [
    path(
        "api/reports/medical-entries/monthly/",
        views.monthly_report,
        name="monthly_report",
    ),
    path(
        "api/reports/medical-entries/interval/<uuid:pk>/",
        views.student_interval_report,
        name="student_interval_report",
    ),
    path(
        "api/reports/report-logs",
        views.view_history,
        name="history_log",
    ),
]
