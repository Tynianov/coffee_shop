from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter(trailing_slash=False)
router.register('branches', RestaurantBranchViewSet, basename='branches')

urlpatterns = [
    path('config', RestaurantConfigView.as_view(), name='restaurant-config'),
    path('terms-and-conditions', TnCView.as_view(), name='terms-and-conditions'),
    path('web-page-config', WebPageConfigView.as_view(), name='web-page-config'),

    re_path(r'^', include(router.urls)),
]
