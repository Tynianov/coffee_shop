from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import ScanLogEntry
from .serializers import ScanLogEntrySerializer


class ScanLogEntryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        log_entries_qs = ScanLogEntry.objects.get_for_initiator(request.user)
        return Response(ScanLogEntrySerializer(log_entries_qs, many=True).data)
