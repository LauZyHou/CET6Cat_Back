from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

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
