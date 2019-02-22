from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from goods.models import Goods
from goods.serializers import GoodsSerializer


class GoodsPagination(PageNumberPagination):
    """自定义分页,用于商品的分页"""
    # 每页多少条记录(这里应该适应前端)
    page_size = 3
    # 可以在url参数中使用'page_size='来指定上面那个page_size的值
    page_size_query_param = 'page_size'
    # 这里指定的是分页时,页面url里表明在哪一页的参数名
    page_query_param = 'page'
    max_page_size = 100


class GoodsViewSet(mixins.ListModelMixin,  # 列表(一堆有序的商品)
                   mixins.RetrieveModelMixin,  # 详情(单个商品)
                   viewsets.GenericViewSet):
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Goods.objects.all()
    # filter_fields = ('name', 'shop_price')
    # filter_class = GoodsFilter
    search_fields = ('name', 'click_num')
    ordering_fields = ('sold_num', 'click_num')
    # 设置默认的排序规则,以用于分页
    ordering = ('id',)
    # 设置Token认证.这里改用JWT认证了,将它注解掉
    # authentication_classes = (TokenAuthentication, )
