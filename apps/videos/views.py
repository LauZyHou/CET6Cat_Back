from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from videos.models import Video
from videos.serializers import VideoSerializer, VideoDetailSerializer


class VideoPagination(PageNumberPagination):
    """视频分页"""
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class VideoViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """视频列表/详情"""
    serializer_class = None
    pagination_class = VideoPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Video.objects.all()
    search_fields = ('name',)
    ordering = ('id',)

    def get_serializer_class(self):
        """list和retrieve的Serializer分开"""
        if self.action == 'list':
            return VideoSerializer
        else:
            return VideoDetailSerializer


class HotVideoViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """首页展示的视频"""
    queryset = Video.objects.all().order_by("hot_value")
    serializer_class = VideoSerializer

    def list(self, request, *args, **kwargs):
        """获取热门视频列表"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 至多取前8个视频
        return Response(serializer.data[:8])
