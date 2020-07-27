from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter(trailing_slash=False)
router.register('list', PostViewSet, basename='posts')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
