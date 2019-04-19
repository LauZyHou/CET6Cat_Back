from rest_framework import mixins, permissions, authentication
from rest_framework import viewsets, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from favorites.models import Watch, FavPost, FavVideo, FavReading, FavEssay
from favorites.serializers import MyWatchSerializer, MyWatchDetailSerializer
from favorites.serializers import WatchMeDetailSerializer
from favorites.serializers import FavPostSerializer, FavPostDetailSerializer
from favorites.serializers import FavVideoSerializer, FavVideoDetailSerializer
from favorites.serializers import FavReadingSerializer, FavReadingDetailSerializer
from favorites.serializers import FavEssaySerializer, FavEssayDetailSerializer


# ---------------------------------[分页]-----------------------------------------

class FavPagination(PageNumberPagination):
    """收藏xx的分页,一页6条"""
    page_size = 6
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 10


# ---------------------------------[我关注的人]-----------------------------------------

class MyWatchViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
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
        if self.action == 'list' or self.action == 'retrieve':
            return MyWatchDetailSerializer
        return MyWatchSerializer

    def get_queryset(self):
        """
        retrieve时:只返回指定用户关注的条目
        list或其它时:只返回我关注的条目
        """
        if self.action == 'retrieve':
            return Watch.objects.filter(uper=self.kwargs['pk']).order_by("id")
        return Watch.objects.filter(uper=self.request.user.id).order_by("id")

    def create(self, request, *args, **kwargs):
        """
        添加：我关注的人
        """
        # 注意,父类的实现中已经调用了is_valid(),这里不用再拿出来调用,只要在Serializer里写好
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我关注的人(传入的是被删除User的id,而不是在Watch表中的id)
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        # instance = self.get_object()
        instance = Watch.objects.filter(uper=self.request.user.id, base=kwargs['pk'])
        self.perform_destroy(instance)
        return Response({"detail": "删除成功"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        [废弃]列出全部：当前用户关注的人
        """
        return super().list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        列出全部：指定用户关注的人
        """
        # 注意!这里实际仍然用list,只是投机地用了REST风格,当指定id时获取那个用户关注的人!
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 重整结构:取出base字段,作为返回列表的每一项
            myres = [item['base'] for item in serializer.data]
            return self.get_paginated_response(myres)

        serializer = self.get_serializer(queryset, many=True)
        # 重整结构:取出base字段,作为返回列表的每一项
        myres = [item['base'] for item in serializer.data]
        return Response(myres)


# ---------------------------------[关注我的人]-----------------------------------------

class WatchMeViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """关注我的人 list时向此view请求"""
    # 用户认证(普通用户从CET6Cat登录用的是JWT,管理员用户从XAdmin登录用的是Session)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # 访问权限认证:已登录.这对针对该view的所有HTTP方法都适用
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WatchMeDetailSerializer

    def get_queryset(self):
        """
        list时:只返回关注我的条目
        retrieve时:只返回关注指定用户的条目
        """
        if self.action == 'list':
            return Watch.objects.filter(base=self.request.user.id).order_by("id")
        return Watch.objects.filter(base=self.kwargs['pk']).order_by("id")

    def list(self, request, *args, **kwargs):
        """
        [废弃]列出全部：关注当前用户的人
        """
        return super().list(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        列出全部：关注指定用户的人
        """
        # 注意!这里实际仍然用list,只是投机地用了REST风格,当指定id时获取那个用户关注的人!
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 重整结构:取出base字段,作为返回列表的每一项
            myres = [item['uper'] for item in serializer.data]
            return self.get_paginated_response(myres)

        serializer = self.get_serializer(queryset, many=True)
        # 重整结构:取出base字段,作为返回列表的每一项
        myres = [item['uper'] for item in serializer.data]
        return Response(myres)


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
    # 分页
    pagination_class = FavPagination

    def get_serializer_class(self):
        """动态获取序列化类"""
        if self.action == 'list':
            return FavPostDetailSerializer
        return FavPostSerializer

    def get_queryset(self):
        """只返回我关注的条目"""
        return FavPost.objects.filter(uper=self.request.user.id).order_by("id")

    def create(self, request, *args, **kwargs):
        """
        添加：我收藏的帖子
        """
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我收藏的帖子(传入的是帖子的id,而不是在收藏表中的id)
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        # instance = self.get_object()
        instance = FavPost.objects.filter(uper=self.request.user.id, base=kwargs['pk'])
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
    # 分页
    pagination_class = FavPagination

    def get_serializer_class(self):
        """动态获取序列化类"""
        if self.action == 'list':
            return FavVideoDetailSerializer
        return FavVideoSerializer

    def get_queryset(self):
        """只返回我关注的条目"""
        return FavVideo.objects.filter(uper=self.request.user.id).order_by("id")

    def create(self, request, *args, **kwargs):
        """
        添加：我收藏的视频
        """
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我收藏的视频(传入的是视频的id,而不是在收藏表中的id)
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        # instance = self.get_object()
        instance = FavVideo.objects.filter(uper=self.request.user.id, base=kwargs['pk'])
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
    # 分页
    pagination_class = FavPagination

    def get_serializer_class(self):
        """动态获取序列化类"""
        if self.action == 'list':
            return FavReadingDetailSerializer
        return FavReadingSerializer

    def get_queryset(self):
        """只返回我关注的条目"""
        return FavReading.objects.filter(uper=self.request.user.id).order_by("id")

    def create(self, request, *args, **kwargs):
        """
        添加：我收藏的文章
        """
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我收藏的文章(传入的是文章的id,而不是在收藏表中的id)
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        # instance = self.get_object()
        instance = FavReading.objects.filter(uper=self.request.user.id, base=kwargs['pk'])
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
    # 分页
    pagination_class = FavPagination

    def get_serializer_class(self):
        """动态获取序列化类"""
        if self.action == 'list':
            return FavEssayDetailSerializer
        return FavEssaySerializer

    def get_queryset(self):
        """只返回我关注的条目"""
        return FavEssay.objects.filter(uper=self.request.user.id).order_by("id")

    def create(self, request, *args, **kwargs):
        """
        添加：我收藏的作文
        """
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除：我收藏的作文(传入的是作文的id,而不是在收藏表中的id)
        注意文档中的DELETE方法的接口测试起来有问题，可以用Postman测试
        """
        # instance = self.get_object()
        instance = FavEssay.objects.filter(uper=self.request.user.id, base=kwargs['pk'])
        self.perform_destroy(instance)
        return Response({"detail": "删除成功"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        列出全部：我收藏的作文
        """
        return super().list(request, args, kwargs)

# ---------------------------------[]-----------------------------------------
