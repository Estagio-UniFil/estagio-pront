from django.http import HttpResponse
from rest_framework.decorators import api_view
from openpyxl import Workbook
from medicalentry.models import MedicalEntry
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime
from students.models import Student
from django.shortcuts import get_object_or_404
from django.utils import timezone
import calendar


@api_view(["GET"])
def monthly_report(request):
    """
    Generate a montly report of all entries in the current or the especified month
    """

    today = date.today()
    year = today.year
    month = today.month

    if request.query_params:
        try:
            year_param = request.query_params.get("year")
            month_param = request.query_params.get("month")

            if year_param and month_param:
                year = int(year_param)
                month = int(month_param)
        except (ValueError, TypeError):
            return Response(
                {"detail": "Parameters must be integers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    entries = MedicalEntry.objects.filter(
        entry_date__year=int(year),
        entry_date__month=int(month),
    ).order_by("entry_date")

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Relatório Mensal"

    headers = ["ID", "Estudante", "Profissional", "Data da Entrada", "Descrição"]
    sheet.append(headers)

    for entry in entries:
        entry_datetime_no_tz = entry.entry_date.replace(tzinfo=None)

        row_data = [
            entry.id,
            entry.student.name,
            entry.healthpro.get_full_name(),
            entry_datetime_no_tz,
            entry.description,
        ]
        sheet.append(row_data)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="relatorio_mensal_{year}-{month}.xlsx"'
    )

    workbook.save(response)

    return response


@api_view(["GET"])
def student_interval_report(request, pk):
    """
    Generate a interval report of all entries for a specific student.
    """

    student_obj = get_object_or_404(Student, pk=pk)

    start_date_str = request.query_params.get("start_date")
    end_date_str = request.query_params.get("end_date")

    # Parse date string to datetime
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(
                hour=23, minute=59, second=59
            )
        except (ValueError, TypeError):
            return Response(
                {"detail": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        # Default
        today = timezone.now()
        start_date = today.replace(day=1, hour=0, minute=0, second=0)
        _, last_day = calendar.monthrange(today.year, today.month)
        end_date = today.replace(day=last_day, hour=23, minute=59, second=59)

    entries = MedicalEntry.objects.filter(
        entry_date__range=(start_date, end_date),
        student=student_obj,
    ).order_by("entry_date")

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = f"Relatório - {student_obj.name}"

    headers = ["ID", "Estudante", "Profissional", "Data da Entrada", "Descrição"]
    sheet.append(headers)

    for entry in entries:
        entry_datetime_no_tz = entry.entry_date.replace(tzinfo=None)

        row_data = [
            entry.id,
            entry.student.name,
            entry.healthpro.get_full_name(),
            entry_datetime_no_tz,
            entry.description,
        ]
        sheet.append(row_data)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    filename = f"relatorio_{student_obj.name}_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    workbook.save(response)

    return response
