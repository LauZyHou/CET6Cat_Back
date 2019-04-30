import datetime

from rest_framework import mixins, permissions, authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from posts.models import Post, Reply
from posts.serializers import PostSerializer, PostDetailSerializer, \
    PostAddSerializer, HotPostSerializer, ReplyDetailSerializer
from favorites.models import FavPost
from db_tools.redis_pool import RedisPool
from db_tools.mongo_pool import StudyNumDump
from CET6Cat.settings import REDIS_THRESHOLD


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
    """帖子:发帖/列表/详情"""
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
        # 不需要指定时间,创建模型时自动就用default了
        # request.data["add_time"] = datetime.datetime.now()
        # 不论传来的用户id是多少,这个帖子必须是当前登录用户发的,防止伪造请求
        request.data["uper"] = request.user.id
        return super().create(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        """获取帖子列表"""
        return super().list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """获取帖子详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 访问该资源时,该资源热度+1(用Redis做优化)
        r = RedisPool.get_connection()
        r_name = 'post_' + kwargs['pk']
        r_val = r.get(r_name)
        if r_val is None:
            r_val = 1
        elif int(r_val) == REDIS_THRESHOLD - 1:
            instance.hot_value += REDIS_THRESHOLD
            instance.save()
            r_val = 0
        else:
            r_val = int(r_val) + 1
        r.set(r_name, r_val)

        # 用户的id,可用于判定是否登录,以及做相应操作
        # 注意,这里不能用self.request.user是否为None判断,因为即使没登录它也是一个AnonymousUser对象
        uid = self.request.user.id

        # 如果用户登录了,本周其访问此资源应+1
        if uid is not None:
            StudyNumDump.dump('forum', uid)

        # 如果用户登录了,额外添加用户是否收藏该帖子(用户没登录时,使用前端默认提供的false)
        if uid is not None:
            find_fav = FavPost.objects.filter(uper=uid, base=kwargs['pk']).count()
            # 没法直接写入非列表形式的serializer.data,这里转dict再加入
            res_dict = dict(serializer.data)
            res_dict["isFaved"] = find_fav > 0  # 实际上这里非0即1
            return Response(res_dict)
        return Response(serializer.data)


class HotPostViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """热门帖子"""
    serializer_class = HotPostSerializer
    queryset = Post.objects.all().order_by("-hot_value")

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


class ReplyViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """回帖:创建"""
    serializer_class = ReplyDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """创建回帖"""
        # 不论传来的用户id是多少,这一楼必须是当前登录用户回的,防止伪造请求
        request.data["uper"] = request.user.id
        return super().create(request, args, kwargs)
