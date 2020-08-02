from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .serializers import *


class CategoriesViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = ProductCategory.objects.active()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.kwargs.get(self.lookup_field, None):
            return ProductCategoryDetailsSerializer
        return ProductCategoryListSerializer


class ProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Product.objects.active()
    lookup_field = 'id'
    serializer_class = ProductSerializer
