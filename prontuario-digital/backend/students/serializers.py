from rest_framework import serializers
from .models import Student
from utils import validators


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

    def validate_guardian_cpf(self, value):
        cpf_validator = validators.cpf()
        if value and not cpf_validator.validate_cpf(value):
            raise serializers.ValidationError("CPF inválido")
        return value
