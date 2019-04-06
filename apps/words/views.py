from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import viewsets

from words.serializers import WordSerializer
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
