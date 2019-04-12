from rest_framework import serializers

from readings.models import Reading


class ReadingSerializer(serializers.ModelSerializer):
    """文章list用这个Serializer"""
    source_name = serializers.CharField(source="source.name")
    source_url = serializers.URLField(source="source.url")

    # 不带文章详细内容content
    class Meta:
        model = Reading
        fields = ("id", "name", "source_name", "source_url", "add_time")


class ReadingDetailSerializer(serializers.ModelSerializer):
    """文章retrieve用这个Serializer"""
    source_name = serializers.CharField(source="source.name")
    source_url = serializers.URLField(source="source.url")

    class Meta:
        model = Reading
        fields = "__all__"


class HotReadingSerializer(serializers.ModelSerializer):
    """热门文章list用这个Serializer"""

    class Meta:
        model = Reading
        fields = ("id", "name", "add_time", "hot_value")
