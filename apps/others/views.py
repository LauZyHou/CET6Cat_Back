from rest_framework import viewsets
from rest_framework.response import Response

from others.models import Banner
from others.serializers import BannerSerializer


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
