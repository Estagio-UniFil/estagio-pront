from django.contrib import admin
from .models import ReportLog


@admin.register(ReportLog)
class ReportLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "date",
        "report_type",
    )
    list_filter = (
        "report_type",
        "date",
    )
    search_fields = (
        "user_id__username",
        "report_type",
    )
    readonly_fields = (
        "id",
        "user_id",
        "date",
        "report_type",
    )
    ordering = ("-date",)
