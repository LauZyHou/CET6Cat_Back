from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Post
from posts.serializers import PostSerializer, PostDetailSerializer


class PostPagination(PageNumberPagination):
    """帖子分页"""
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class PostViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """帖子列表/详情"""
    serializer_class = None
    pagination_class = PostPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Post.objects.all()
    search_fields = ('name',)
    ordering = ('id',)

    def get_serializer_class(self):
        """list和retrieve的Serializer分开"""
        if self.action == 'list':
            return PostSerializer
        else:
            return PostDetailSerializer
