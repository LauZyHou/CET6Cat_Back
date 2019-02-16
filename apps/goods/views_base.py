# 引入Model
from goods.models import Goods

# Django CBV方式最底层的view
from django.views.generic.base import View


class GoodsListView(View):
    """
    商品list视图
    """

    def get(self, request):
        """
        获取商品list信息
        """
        json_list = []  # 存放商品字典的列表
        goods = Goods.objects.all()  # 从数据库中读取所有商品

        from django.forms.models import model_to_dict  # 该方法用于将model转换为python字典
        for good in goods:  # 对每个商品实现转化,写入列表中
            json_dict = model_to_dict(good)
            json_list.append(json_dict)

        import json
        from django.core import serializers  # 用于序列化为JSON字符串
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        from django.http import HttpResponse, JsonResponse
        # jsonResponse做的工作也就是加上了dumps和content_type
        # return HttpResponse(json.dumps(json_data), content_type="application/json")
        # 注释掉loads，下面语句正常
        # return HttpResponse(json_data, content_type="application/json")
        # 返回的不为dict时要设置safe=False(这里是一个JSON数组,不是标准JSON格式)
        return JsonResponse(json_data, safe=False)
