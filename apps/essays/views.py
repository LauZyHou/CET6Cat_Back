from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from essays.models import Essay
from essays.serializers import EssaySerializer, EssayDetailSerializer


class EssayPagination(PageNumberPagination):
    """作文分页"""
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class EssayViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """作文列表/详情"""
    serializer_class = None
    pagination_class = EssayPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Essay.objects.all()
    search_fields = ('name',)
    ordering = ('id',)

    def get_serializer_class(self):
        """list和retrieve的Serializer分开"""
        if self.action == 'list':
            return EssaySerializer
        else:
            return EssayDetailSerializer
