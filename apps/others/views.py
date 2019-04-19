from rest_framework import viewsets, mixins, permissions, authentication
from rest_framework.response import Response

from others.models import Banner, Audio, Translate
from others.serializers import BannerSerializer
from users.models import UserProfile
from readings.models import Reading
from videos.models import Video
from posts.models import Post
from essays.models import Essay
from others.serializers import AudioSerializer, AudioDetailSerializer, TranslateSerializer, TranslateDetailSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class BannerViewSet(viewsets.ViewSet):
    """轮播图list走此ViewSet"""

    def list(self, request):
        """获取轮播图(按轮播顺序)"""
        queryset = Banner.objects.all().order_by("-index", "-id")  # 先按index降序,index相同的按id降序
        serializer = BannerSerializer(queryset, many=True)
        # 轮播图最多返回4个
        if len(serializer.data) > 3:
            return Response(serializer.data[0:4])
        return Response(serializer.data)


class GlobalSearchViewSet(viewsets.ViewSet):
    """全局模糊查询(用户/文章/视频/帖子/作文)"""

    def list(self, request):
        """全局模糊查询,传入url参数s=搜索内容"""
        # 请求[.../globalsearch/?s=请求内容]
        s = request.query_params.get('s')
        ret = {"users": [], "readings": [], "videos": [], "posts": [], "essays": []}
        # 查找用户
        user_queryset = UserProfile.objects.filter(name__contains=s)
        for q in user_queryset:
            ret["users"].append({'id': q.id, 'name': q.name})
        # 查找文章
        reading_queryset = Reading.objects.filter(name__contains=s)
        for q in reading_queryset:
            ret["readings"].append({'id': q.id, 'name': q.name})
        # 查找视频
        video_queryset = Video.objects.filter(name__contains=s)
        for q in video_queryset:
            ret["videos"].append({'id': q.id, 'name': q.name})
        # 查找帖子
        post_queryset = Post.objects.filter(name__contains=s)
        for q in post_queryset:
            ret["posts"].append({'id': q.id, 'name': q.name})
        # 查找作文
        essay_queryset = Essay.objects.filter(name__contains=s)
        for q in essay_queryset:
            ret["essays"].append({'id': q.id, 'name': q.name})
        return Response(ret)


class AudioViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """听力list/retrieve"""
    queryset = Audio.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return AudioSerializer
        return AudioDetailSerializer

    def list(self, request, *args, **kwargs):
        """听力资源列表"""
        return super().list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """听力资源详细内容"""
        return super().retrieve(request, args, kwargs)


class TranslateViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """翻译list/retrieve"""
    queryset = Translate.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return TranslateSerializer
        return TranslateDetailSerializer

    def list(self, request, *args, **kwargs):
        """翻译资源列表"""
        return super().list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """翻译资源详细内容"""
        return super().retrieve(request, args, kwargs)
