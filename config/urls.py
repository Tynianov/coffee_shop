from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter(trailing_slash=False)
router.register('branches', RestaurantBranchViewSet, basename='branches')

urlpatterns = [
    path('config', RestaurantConfigView.as_view(), name='restaurant-config'),

    re_path(r'^', include(router.urls)),
]
