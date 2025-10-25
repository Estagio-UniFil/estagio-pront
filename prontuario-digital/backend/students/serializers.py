from rest_framework import serializers
from .models import Student
from datetime import date


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "cgm",
            "dob",
            "gender",
            "guardian",
            "guardian_cpf",
            "address",
            "cep",
            "city",
            "state",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "active",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]

        def validate_dob(self, value):
            """
            Verify if dob is not on the future.
            """
            if value > date.today():
                raise serializers.ValidationError(
                    "A data de nascimento não pode ser no futuro."
                )
            return value


class StudentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "cgm", "dob"]
