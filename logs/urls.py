from django.urls import path

from .views import *

urlpatterns = [
    path('list', ScanLogEntryView.as_view(), name='log-list')
]