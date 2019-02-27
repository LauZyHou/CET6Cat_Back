from rest_framework import serializers

from videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    """视频list用这个Serializer"""

    # 不带视频详细内容content
    class Meta:
        model = Video
        fields = ("id", "name", "thumb", "category", "add_time")


class VideoDetailSerializer(serializers.ModelSerializer):
    """视频retrieve用这个Serializer"""

    class Meta:
        model = Video
        fields = ("id", "name", "content", "category", "uper", "add_time")
