from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .models import RestaurantConfig, RestaurantBranch
from .serializers import \
    RestaurantBranchDetailsSerializer,\
    RestaurantConfigSerializers


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
