from rest_framework import serializers
from .models import MedicalEntry
from authentication.serializers import UserNestedSerializer
from students.serializers import StudentNestedSerializer


class MedicalEntrySerializer(serializers.ModelSerializer):
    student = StudentNestedSerializer(read_only=True)
    healthpro = UserNestedSerializer(read_only=True)

    class Meta:
        model = MedicalEntry
        fields = [
            "id",
            "student",
            "healthpro",
            "entry_date",
            "description",
            "notes",
            "deleted",
            "deleted_by",
            "delete_date",
            "delete_reason",
        ]
        read_only_fields = [
            "id",
            "student",
            "healthpro",
            "entry_date",
            "deleted",
            "deleted_by",
            "delete_date",
            "delete_reason",
        ]

    def create(self, validated_data):
        validated_data["healthpro"] = self.context["request"].user
        return super().create(validated_data)
