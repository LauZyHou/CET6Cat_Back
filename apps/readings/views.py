from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from readings.models import Reading
from readings.serializers import ReadingSerializer, ReadingDetailSerializer


class ReadingPagination(PageNumberPagination):
    """文章分页"""
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class ReadingViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """文章列表/详情"""
    serializer_class = None
    pagination_class = ReadingPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Reading.objects.all()
    search_fields = ('name',)
    ordering = ('id',)

    def get_serializer_class(self):
        """list和retrieve的Serializer分开"""
        if self.action == 'list':
            return ReadingSerializer
        else:
            return ReadingDetailSerializer


class HotReadingViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """热门文章"""
    serializer_class = ReadingSerializer
    queryset = Reading.objects.all().order_by("hot_value")

    def list(self, request, *args, **kwargs):
        """获取热门文章列表"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 至多返回8条
        return Response(serializer.data[:8])
