from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from readings.models import Reading
from readings.serializers import ReadingSerializer, ReadingDetailSerializer, HotReadingSerializer
from favorites.models import FavReading


class ReadingPagination(PageNumberPagination):
    """文章分页"""
    page_size = 7
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class ReadingViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """文章:列表/详情"""
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

    def list(self, request, *args, **kwargs):
        """获取文章列表"""
        return super().list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """获取文章详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 访问该资源时,该资源热度+1.fixme 改用redis每+10再写入数据库
        instance.hot_value += 1
        instance.save()
        # 如果用户登录了,额外添加用户是否收藏该文章(用户没登录时,使用前端默认提供的false)
        # 注意,这里不能用self.request.user是否为None判断,因为即使没登录它也是一个AnonymousUser对象
        if self.request.user.id is not None:
            find_fav = FavReading.objects.filter(uper=self.request.user.id, base=kwargs['pk']).count()
            # 没法直接写入非列表形式的serializer.data,这里转dict再加入
            res_dict = dict(serializer.data)
            res_dict["isFaved"] = find_fav > 0  # 实际上这里非0即1
            return Response(res_dict)
        return Response(serializer.data)


class HotReadingViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """热门文章"""
    serializer_class = HotReadingSerializer
    queryset = Reading.objects.all().order_by("-hot_value")

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
