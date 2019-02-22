from rest_framework import serializers
from goods.models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    """商品序列化"""

    # 这里自己定义字段去覆盖自动序列化的字段

    class Meta:
        model = Goods
        fields = "__all__"
