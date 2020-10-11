from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .serializers import *


class CategoriesViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = ProductCategory.objects.active()
    lookup_field = 'id'
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.kwargs.get(self.lookup_field, None):
            return ProductCategoryDetailsSerializer
        return ProductCategoryListSerializer


class ProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Product.objects.active()
    lookup_field = 'id'
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class CategoryProductList(ListAPIView):

    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        category_id = self.kwargs.get('id')
        category = ProductCategory.objects.filter(id=category_id).first()
        if not category:
            return Response(status=HTTP_404_NOT_FOUND)

        qs = Product.objects.filter(category_id=category_id)
        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data)
