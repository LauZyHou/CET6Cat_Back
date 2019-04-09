import random

from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response

from words.serializers import WordSerializer, WordCloudSerializer
from words.models import Word


class WordsPagination(PageNumberPagination):
    """帖子分页"""
    page_size = 20  # 一组20个单词
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 120  # 一共是103组,这里稍设大一点,以后可能往库里添加单词


class WordsViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """单词视图"""
    pagination_class = WordsPagination
    serializer_class = WordSerializer
    queryset = Word.objects.all().order_by("id")

    def list(self, request, *args, **kwargs):
        """获取数据库中的单词"""
        return super().list(request, args, kwargs)


class WordCloudViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """词云视图"""
    serializer_class = WordCloudSerializer
    # 从1~1060中随机取30个数得到id列表,取id在这个列表中的那些单词
    queryset = Word.objects.filter(id__in=random.sample(range(1, 1060), 30))

    def list(self, request, *args, **kwargs):
        """获取词云单词"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # fixme 这里暂时用这种方式添加value指数
        for k in serializer.data:
            k["value"] = random.randint(1, 300)
            del k["id"]
        return Response(serializer.data)
