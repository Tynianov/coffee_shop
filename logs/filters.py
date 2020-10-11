from datetime import datetime, timedelta
import django_filters

from .models import ScanLogEntry


class ScanLogEntryFilter(django_filters.FilterSet):
    created = django_filters.DateTimeFilter(method='filter_created')

    class Meta:
        model = ScanLogEntry
        fields = ['created']

    def filter_created(self, queryset, name, value):
        if not value:
            return queryset
        last_day = value - timedelta(days=1)
        return queryset.filter(created__range=[last_day, value])
