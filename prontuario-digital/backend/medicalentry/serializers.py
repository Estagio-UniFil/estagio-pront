from rest_framework import serializers
from .models import MedicalEntry


class MedicalEntrySerializer(serializers.ModelSerializer):
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
