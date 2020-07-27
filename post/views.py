from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .serializers import PostListSerializer, PostDetailsSerializer
from .models import Post


class PostViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Post.objects.active()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.kwargs.get(self.lookup_field, None):
            return PostDetailsSerializer
        return PostListSerializer

