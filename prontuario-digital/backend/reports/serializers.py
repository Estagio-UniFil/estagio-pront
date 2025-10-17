from rest_framework import serializers
from .models import ReportLog
from authentication.serializers import UserNestedSerializer


class ReportLogSerializer(serializers.ModelSerializer):
    user_id = UserNestedSerializer(read_only=True)

    class Meta:
        model = ReportLog
        fields = "__all__"
