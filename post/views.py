from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .serializers import PostListSerializer, PostConfigSerializer
from .models import Post, PostConfig


class PostViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Post.objects.active()
    lookup_field = 'id'
    serializer_class = PostListSerializer


class PostConfigView(APIView):

    def get(self, request):
        config = PostConfig.get_solo()
        return Response(PostConfigSerializer(config).data)
