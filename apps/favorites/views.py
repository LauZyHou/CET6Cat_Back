from rest_framework import mixins, permissions, authentication
from rest_framework import viewsets, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response

from favorites.models import Watch, FavPost, FavVideo, FavReading, FavEssay
from favorites.serializers import MyWatchSerializer, MyWatchDetailSerializer
from favorites.serializers import WatchMeDetailSerializer
from favorites.serializers import FavPostSerializer, FavPostDetailSerializer
from favorites.serializers import FavVideoSerializer, FavVideoDetailSerializer
from favorites.serializers import FavReadingSerializer, FavReadingDetailSerializer
from favorites.serializers import FavEssaySerializer, FavEssayDetailSerializer


# ---------------------------------[我关注的人]-----------------------------------------

class MyWatchViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    我关注的人 create,destroy,list时向此view请求
    """
    # 用户认证(普通用户从CET6Cat登录用的是JWT,管理员用户从XAdmin登录用的是Session)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # 访问权限认证:已登录.这对针对该view的所有HTTP方法都适用
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        """动态获取序列化类"""
        if self.action == 'list':
            return MyWatchDetailSerializer
        return MyWatchSerializer

    def get_queryset(self):
        """只返回我关注的条目"""
        return Watch.objects.filter(uper=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """
        添加：我关注的人
        """
        # 注意,父类的实现中已经调用了is_valid(),这里不用再拿出来调用,只要在Serializer里写好
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我关注的人
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "删除成功"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        列出全部：我关注的人
        """
        return super().list(request, args, kwargs)


# ---------------------------------[关注我的人]-----------------------------------------

class WatchMeViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """关注我的人 list时向此view请求"""
    # 用户认证(普通用户从CET6Cat登录用的是JWT,管理员用户从XAdmin登录用的是Session)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # 访问权限认证:已登录.这对针对该view的所有HTTP方法都适用
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WatchMeDetailSerializer

    def get_queryset(self):
        """只返回关注我的条目"""
        return Watch.objects.filter(base=self.request.user.id)

    def list(self, request, *args, **kwargs):
        """
        列出全部：关注我的人
        """
        return super().list(request, args, kwargs)


# ---------------------------------[我收藏的帖子]-----------------------------------------

class FavPostViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    我收藏的帖子 create,destroy,list时向此view请求
    """
    # queryset = FavPost.objects.all()

    # 用户认证(普通用户从CET6Cat登录用的是JWT,管理员用户从XAdmin登录用的是Session)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # 访问权限认证:已登录.这对针对该view的所有HTTP方法都适用
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        """动态获取序列化类"""
        if self.action == 'list':
            return FavPostDetailSerializer
        return FavPostSerializer

    def get_queryset(self):
        """只返回我关注的条目"""
        return FavPost.objects.filter(uper=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """
        添加：我收藏的帖子
        """
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我收藏的帖子
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "删除成功"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        列出全部：我收藏的帖子
        """
        return super().list(request, args, kwargs)


# ---------------------------------[我收藏的视频]-----------------------------------------

class FavVideoViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    我收藏的视频 create,destroy,list时向此view请求
    """
    # 用户认证(普通用户从CET6Cat登录用的是JWT,管理员用户从XAdmin登录用的是Session)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # 访问权限认证:已登录.这对针对该view的所有HTTP方法都适用
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        """动态获取序列化类"""
        if self.action == 'list':
            return FavVideoDetailSerializer
        return FavVideoSerializer

    def get_queryset(self):
        """只返回我关注的条目"""
        return FavVideo.objects.filter(uper=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """
        添加：我收藏的视频
        """
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我收藏的视频
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "删除成功"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        列出全部：我收藏的视频
        """
        return super().list(request, args, kwargs)


# ---------------------------------[我收藏的文章]-----------------------------------------

class FavReadingViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    我收藏的文章 create,destroy,list时向此view请求
    """
    # 用户认证(普通用户从CET6Cat登录用的是JWT,管理员用户从XAdmin登录用的是Session)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # 访问权限认证:已登录.这对针对该view的所有HTTP方法都适用
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        """动态获取序列化类"""
        if self.action == 'list':
            return FavReadingDetailSerializer
        return FavReadingSerializer

    def get_queryset(self):
        """只返回我关注的条目"""
        return FavReading.objects.filter(uper=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """
        添加：我收藏的文章
        """
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我收藏的文章
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "删除成功"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        列出全部：我收藏的文章
        """
        return super().list(request, args, kwargs)


# ---------------------------------[我收藏的作文]-----------------------------------------

class FavEssayViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    我收藏的作文 create,destroy,list时向此view请求
    """
    # 用户认证(普通用户从CET6Cat登录用的是JWT,管理员用户从XAdmin登录用的是Session)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # 访问权限认证:已登录.这对针对该view的所有HTTP方法都适用
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        """动态获取序列化类"""
        if self.action == 'list':
            return FavEssayDetailSerializer
        return FavEssaySerializer

    def get_queryset(self):
        """只返回我关注的条目"""
        return FavEssay.objects.filter(uper=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """
        添加：我收藏的作文
        """
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我收藏的作文
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "删除成功"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        列出全部：我收藏的作文
        """
        return super().list(request, args, kwargs)

# ---------------------------------[]-----------------------------------------
