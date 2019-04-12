from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from essays.models import Essay
from essays.serializers import EssaySerializer, EssayDetailSerializer
from favorites.models import FavEssay


class EssayPagination(PageNumberPagination):
    """作文分页"""
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class EssayViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """作文:列表/详情"""
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

    def list(self, request, *args, **kwargs):
        """获取作文列表"""
        return super().list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """获取作文详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 如果用户登录了,额外添加用户是否收藏该作文(用户没登录时,使用前端默认提供的false)
        # 注意,这里不能用self.request.user是否为None判断,因为即使没登录它也是一个AnonymousUser对象
        if self.request.user.id is not None:
            find_fav = FavEssay.objects.filter(uper=self.request.user.id, base=kwargs['pk']).count()
            # 没法直接写入非列表形式的serializer.data,这里转dict再加入
            res_dict = dict(serializer.data)
            res_dict["isFaved"] = find_fav > 0  # 实际上这里非0即1
            return Response(res_dict)
        return Response(serializer.data)


class HotEssayViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """热门作文"""
    serializer_class = EssaySerializer
    queryset = Essay.objects.all().order_by("hot_value")

    def list(self, request, *args, **kwargs):
        """获取热门作文列表"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 至多返回8条
        return Response(serializer.data[:8])
