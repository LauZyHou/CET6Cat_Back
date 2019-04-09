import datetime

from rest_framework import mixins, permissions, authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from posts.models import Post
from posts.serializers import PostSerializer, PostDetailSerializer, PostAddSerializer


class PostPagination(PageNumberPagination):
    """帖子分页"""
    page_size = 3
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class PostViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """帖子列表/详情"""
    serializer_class = None
    pagination_class = PostPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Post.objects.all()
    search_fields = ('name',)
    ordering = ('id',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        """覆写,以在不同的请求方法下使用不同的权限认证"""
        if self.action == "create":
            return [permissions.IsAuthenticated()]  # 登录了才能发帖
        return [permissions.AllowAny()]  # 登不登录都能看贴

    def get_serializer_class(self):
        """list和create和retrieve的Serializer分开"""
        if self.action == 'list':  # 帖子列表
            return PostSerializer
        elif self.action == 'create':  # 发帖
            return PostAddSerializer
        else:  # 帖子详情
            return PostDetailSerializer

    def create(self, request, *args, **kwargs):
        """发帖"""
        request.data["add_time"] = datetime.datetime.now()
        # 不论传来的用户id是多少,这个帖子必须是当前登录用户发的,防止伪造请求
        request.data["uper"] = request.user.id
        return super().create(request, args, kwargs)


class HotPostViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """热门帖子"""
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by("hot_value")

    def list(self, request, *args, **kwargs):
        """获取热门帖子列表"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 至多返回8条
        return Response(serializer.data[:8])
