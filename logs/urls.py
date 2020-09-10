from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register('list', ScanLogEntryView, basename='log-list')

urlpatterns = [
    path('', include(router.urls))
]
