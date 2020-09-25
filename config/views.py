from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .models import RestaurantConfig, RestaurantBranch, AppMetadataConfig
from .serializers import \
    RestaurantBranchDetailsSerializer,\
    RestaurantConfigSerializers,\
    TnCSerializer,\
    WebPageConfigSerializer


class RestaurantBranchViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = RestaurantBranch.objects.active()
    lookup_field = 'id'
    serializer_class = RestaurantBranchDetailsSerializer
    pagination_class = None


class RestaurantConfigView(APIView):
    def get(self, request):
        config = RestaurantConfig.get_solo()
        serializer = RestaurantConfigSerializers(config)
        return Response(serializer.data)


class BaseAppMetadataView(RetrieveAPIView):
    permission_classes = [AllowAny]

    def get_object(self):
        obj = AppMetadataConfig.get_solo()
        return obj


class TnCView(BaseAppMetadataView):
    serializer_class = TnCSerializer


class WebPageConfigView(BaseAppMetadataView):
    serializer_class = WebPageConfigSerializer
