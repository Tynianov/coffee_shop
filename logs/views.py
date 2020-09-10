from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser

from .models import ScanLogEntry
from .serializers import ScanLogEntrySerializer
from .filters import ScanLogEntryFilter


class ScanLogEntryView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAdminUser]
    filter_class = ScanLogEntryFilter
    serializer_class = ScanLogEntrySerializer

    def get_queryset(self):
        return ScanLogEntry.objects.get_for_initiator(self.request.user)
