from django.contrib import admin

from .models import ScanLogEntry


@admin.register(ScanLogEntry)
class ScanLogEntryAdmin(admin.ModelAdmin):
    list_display = ['created', 'type', 'status']
