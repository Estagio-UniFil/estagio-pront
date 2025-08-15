from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import MedicalEntry
from .serializers import MedicalEntrySerializer
from students.models import Student
from authentication.permissions import (
    HealthProfWriteAllRead,
    IsAdminOrHealthProfessional,
)


@api_view(["GET", "POST"])
@permission_classes([HealthProfWriteAllRead])
def medical_entry_list(request):
    student_id = request.query_params.get("student_id")
    if student_id:
        try:
            student_obj = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response(
                {"detail": "Student not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    if request.method == "GET":
        if student_id:
            if request.user.role in ["admin", "health_prof"]:
                if request.user.role == "health_prof":
                    if hasattr(request.user, "health_profile"):
                        user_specialty = request.user.health_profile.specialty
                        entries = MedicalEntry.objects.filter(
                            deleted=False,
                            student=student_obj,
                            healthpro__health_profile__specialty=user_specialty,
                        ).order_by("entry_date")
                else:
                    entries = MedicalEntry.objects.filter(
                        deleted=False,
                        student=student_obj,
                    ).order_by("entry_date")
                serializer = MedicalEntrySerializer(entries, many=True)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "You don't have permission"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        else:
            if request.user.role == "health_prof":
                if hasattr(request.user, "health_profile"):
                    user_specialty = request.user.health_profile.specialty
                    entries = MedicalEntry.objects.filter(
                        deleted=False,
                        healthpro__health_profile__specialty=user_specialty,
                    ).order_by("entry_date")
            else:
                entries = MedicalEntry.objects.filter(deleted=False).order_by(
                    "entry_date"
                )
        serializer = MedicalEntrySerializer(entries, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    if request.method == "POST":
        if request.user.role not in ["health_prof"]:
            return Response(
                {"detail": "You don't have permission"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not student_id:
            return Response(
                {"detail": "No informed student"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MedicalEntrySerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(student=student_obj, healthpro=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
@permission_classes([IsAdminOrHealthProfessional])
def medical_entry_detail(request, pk):
    try:
        entry = MedicalEntry.objects.get(pk=pk)
    except MedicalEntry.DoesNotExist:
        return Response(
            {"detail": "Medical entry not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        if entry.deleted:
            return Response(
                {"detail": "Medical entry not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.role == "health_prof":
            if hasattr(request.user, "health_profile"):
                user_specialty = request.user.health_profile.specialty
                if user_specialty != entry.healthpro.health_profile.specialty:
                    return Response(
                        {"detail": "This is not in your scope"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

        serializer = MedicalEntrySerializer(entry)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    if request.method == "DELETE":
        if entry.deleted:
            return Response(
                {"detail": "Entry is already deleted"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        delete_reason = request.data.get("delete_reason")
        if not delete_reason:
            return Response(
                {"detail": "Delete reason is mandatory"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        entry.soft_delete(user=request.user, reason=delete_reason)
        return Response(status=status.HTTP_204_NO_CONTENT)
