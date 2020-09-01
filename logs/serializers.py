from rest_framework import serializers

from .models import ScanLogEntry


class ScanLogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanLogEntry
        fields = '__all__'
