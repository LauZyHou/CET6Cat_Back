import random

from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, permissions, authentication
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from words.serializers import WordSerializer, WordCloudSerializer, WordTrainSerializer
from words.models import Word
from db_tools.mongo_pool import CET6CatDB
from CET6Cat.settings import MAX_WORDS_NUM, FRONT_WORDS_NUM


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


class WordTrainViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """专项训练->单词测验"""
    serializer_class = WordTrainSerializer
    # 从1~1060中随机取40个数得到id列表,取id在这个列表中的那些单词
    queryset = Word.objects.filter(id__in=random.sample(range(1, 1060), 40))
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        """组卷并返回"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        # 生成前端要求的卷子格式(四个一组放在check里,随机带一个正确项)并返回
        res = [{'correct': random.randint(0, 3), 'check': []} for i in range(10)]
        for i, k in enumerate(serializer.data):
            res[i // 4]['check'].append(k)
        return Response(res)

    def create(self, request, *args, **kwargs):
        """用户单词测验上传错误的单词id"""
        # 当前用户id
        uid = request.user.id
        # 当前提交上来的错误单词id
        now_fw = request.data["faultWords"]
        # 当前用户在MongoDB中的文档
        doc = CET6CatDB.fault_words.find_one({'uid': uid})
        # 写入固定最大长度为30,没有记录即该项为None(None只存在于末尾)的数组
        # 为什么长度固定为30?这样避免了使用动态长度时,数据更新使MongoDB存储扩展降低数据库性能
        fw = [None for i in range(MAX_WORDS_NUM)]
        # print(CET6CatDB.fault_words.find_one({'uid': uid}))

        # 查询用户是否有记录,如果没有就插入新记录
        if not doc:
            idx = 0
            for i in range(FRONT_WORDS_NUM):
                if now_fw[i] is None:
                    break
                fw[idx] = now_fw[i]
                idx += 1
            CET6CatDB.fault_words.insert({'uid': uid, 'fault_words': fw})
        # 否则更新错误单词记录
        else:
            # 使用LRU算法,将错误的单词提到最前
            # 此处采取了多插入LRU的一种快速实现,不妨认为传来的0~10个错误单词是等价的,那么先按顺序置于最前
            idx = 0
            no_repeat = set()  # LRU防重复
            # 新错误单词置于最前过程:此过程本无需考虑重复,因为前端获取的40个单词就是不重复的
            # 但为了防止用户修改post的body来传入重复单词id,这里仍用set判断一下
            for i in range(FRONT_WORDS_NUM):
                if now_fw[i] is None:
                    break
                if now_fw[i] in no_repeat:  # 跳过重复单词
                    continue
                fw[idx] = now_fw[i]
                idx += 1
                no_repeat.add(now_fw[i])
            # 数据库中的旧错误单词,按顺序无重复接在后面即得到了LRU多插入结果
            db_fw = doc['fault_words']
            for i in range(MAX_WORDS_NUM):
                if db_fw[i] is None or idx >= MAX_WORDS_NUM:
                    break
                if db_fw[i] in no_repeat:  # 跳过重复单词
                    continue
                fw[idx] = db_fw[i]
                idx += 1
                no_repeat.add(db_fw[i])
            CET6CatDB.fault_words.update({'uid': uid}, {"$set": {'fault_words': fw}})
        print(CET6CatDB.fault_words.find_one({'uid': uid}))
        return Response({'ok': '收到'})

    def retrieve(self, request, *args, **kwargs):
        """获取用户的错误词汇(0~MAX_WORDS_NUM个)"""
        # 当前用户id
        uid = request.user.id
        # 当前用户在MongoDB中的文档
        doc = CET6CatDB.fault_words.find_one({'uid': uid})
        if not doc:
            return Response([])
        # 数据库中的错误单词
        db_fw = doc['fault_words']
        ret_lst = [{'name': Word.objects.get(id=item).name, 'value': random.randint(100, 400)} for item in db_fw if
                   item is not None]
        print(ret_lst)
        return Response(ret_lst)
