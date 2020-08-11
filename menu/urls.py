from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter(trailing_slash=False)
router.register('categories-list', CategoriesViewSet, basename='categories')
router.register('product-details', ProductViewSet, basename='product-details')

urlpatterns = [
    re_path(r'category-product-list/(?P<id>\d+)/$', CategoryProductList.as_view(), name='category-product-list'),
    re_path(r'^', include(router.urls))
]
