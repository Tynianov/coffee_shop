from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .serializers import PostListSerializer, PostDetailsSerializer, PostConfigSerializer
from .models import Post, PostConfig


class PostViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Post.objects.active()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.kwargs.get(self.lookup_field, None):
            return PostDetailsSerializer
        return PostListSerializer


class PostConfigView(APIView):

    def get(self, request):
        config = PostConfig.get_solo()
        return Response(PostConfigSerializer(config).data)
