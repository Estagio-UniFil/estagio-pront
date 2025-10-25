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
    """
    GET: Lista entradas de prontuário (todos podem ver a lista)
    POST: Cria nova entrada (apenas health_prof)
    Query params: student_id (opcional) - filtra por estudante específico
    """

    if request.method == "GET":
        student_id = request.query_params.get("student_id")

        queryset = MedicalEntry.objects.filter(deleted=False)

        if student_id:
            try:
                student_obj = Student.objects.get(pk=student_id)
                queryset = queryset.filter(student=student_obj)
            except Student.DoesNotExist:
                return Response(
                    {"detail": "Student not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        if request.user.role == "health_prof":
            if hasattr(request.user, "health_profile"):
                user_specialty = request.user.health_profile.specialty
                queryset = queryset.filter(
                    healthpro__health_profile__specialty=user_specialty
                )
            else:
                queryset = queryset.none()

        entries = queryset.order_by("-entry_date")

        serializer = MedicalEntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if request.user.role != "health_prof":
            return Response(
                {"detail": "Only health professionals can create entries"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not hasattr(request.user, "health_profile"):
            return Response(
                {"detail": "Health profile not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student_id = request.data.get("student_id")
        if not student_id:
            return Response(
                {"detail": "student_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            student_obj = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response(
                {"detail": "Student not found"},
                status=status.HTTP_404_NOT_FOUND,
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
    """
    GET: Detalhes de uma entrada específica (admin ou health_prof da mesma especialidade)
    DELETE: Soft delete de uma entrada (apenas health_prof com razão obrigatória)
    """

    try:
        entry = MedicalEntry.objects.get(pk=pk, deleted=False)
    except MedicalEntry.DoesNotExist:
        return Response(
            {"detail": "Medical entry not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        if request.user.role == "health_prof":
            if not hasattr(request.user, "health_profile"):
                return Response(
                    {"detail": "Health profile not found"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            user_specialty = request.user.health_profile.specialty

            if not hasattr(entry.healthpro, "health_profile"):
                return Response(
                    {"detail": "Entry creator health profile not found"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            entry_specialty = entry.healthpro.health_profile.specialty

            if user_specialty != entry_specialty:
                return Response(
                    {"detail": "You can only view entries from your specialty"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = MedicalEntrySerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        if request.user.role != "health_prof":
            return Response(
                {"detail": "Only health professionals can delete entries"},
                status=status.HTTP_403_FORBIDDEN,
            )

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
        return Response(
            {"detail": "Entry deleted successfully"}, status=status.HTTP_200_OK
        )


@api_view(["GET"])
@permission_classes([IsAdminOrHealthProfessional])
def medical_entry_by_student(request, student_id):
    """
    Endpoint específico para buscar todas as entradas de um estudante
    Aplica as mesmas regras de permissão da listagem
    """

    try:
        student_obj = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return Response(
            {"detail": "Student not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    queryset = MedicalEntry.objects.filter(student=student_obj, deleted=False)

    if request.user.role == "health_prof":
        if hasattr(request.user, "health_profile"):
            user_specialty = request.user.health_profile.specialty
            queryset = queryset.filter(
                healthpro__health_profile__specialty=user_specialty
            )
        else:
            queryset = queryset.none()

    entries = queryset.order_by("-entry_date")

    serializer = MedicalEntrySerializer(entries, many=True)
    return Response(
        {
            "student_id": student_id,
            "student_name": getattr(student_obj, "name", "N/A"),
            "entries": serializer.data,
        },
        status=status.HTTP_200_OK,
    )
