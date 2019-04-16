from rest_framework import serializers

from videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    视频list用这个Serializer

    [这个Serializer现在有两个View用,一个是普通视频list,一个是首页热门视频list.
    这两个View在前端都没有地方可以展示hot_value,所以这里没返回(和别的资源不太一样)]
    """

    # 不带视频详细内容content
    class Meta:
        model = Video
        fields = ("id", "name", "thumb", "category", "add_time")


class VideoDetailSerializer(serializers.ModelSerializer):
    """视频retrieve用这个Serializer"""

    class Meta:
        model = Video
        fields = ("id", "name", "content", "category", "uper", "add_time", "hot_value")
