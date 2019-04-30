from rest_framework import mixins
from rest_framework import viewsets, authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from videos.models import Video
from favorites.models import FavVideo
from videos.serializers import VideoSerializer, VideoDetailSerializer
from db_tools.redis_pool import RedisPool
from db_tools.mongo_pool import StudyNumDump
from CET6Cat.settings import REDIS_THRESHOLD


class VideoPagination(PageNumberPagination):
    """视频分页"""
    page_size = 8
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
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        """list和retrieve的Serializer分开"""
        if self.action == 'list':
            return VideoSerializer
        else:
            return VideoDetailSerializer

    def list(self, request, *args, **kwargs):
        """获取视频列表"""
        return super().list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """获取视频详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 访问该资源时,该资源热度+1(用Redis做优化)
        r = RedisPool.get_connection()
        r_name = 'video_' + kwargs['pk']
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
            StudyNumDump.dump('video', uid)

        # 如果用户登录了,额外添加字段:用户是否收藏该视频(用户没登录时,使用前端默认提供的false,故不添加此字段)
        if uid is not None:
            find_fav = FavVideo.objects.filter(uper=uid, base=kwargs['pk']).count()
            # 没法直接写入非列表形式的serializer.data,这里转dict再加入
            res_dict = dict(serializer.data)
            res_dict["isFaved"] = find_fav > 0  # 实际上这里非0即1
            return Response(res_dict)
        return Response(serializer.data)


class HotVideoViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """首页展示的视频"""
    queryset = Video.objects.all().order_by("-hot_value")
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
