from rest_framework import serializers

from user.serializers import MinimumUserDataSerializer
from .models import ScanLogEntry


class ScanLogEntrySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ScanLogEntry
        fields = '__all__'

    def get_user(self, obj):
        if obj.user:
            return MinimumUserDataSerializer(obj.user).data
        return
