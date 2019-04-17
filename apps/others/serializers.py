from rest_framework import serializers

from others.models import Banner, Audio


class BannerSerializer(serializers.ModelSerializer):
    """轮播图Serializer"""

    class Meta:
        model = Banner
        fields = "__all__"


class AudioSerializer(serializers.ModelSerializer):
    """听力list用此Serializer"""

    class Meta:
        model = Audio
        fields = ("id", "name")


class AudioDetailSerializer(serializers.ModelSerializer):
    """听力retrieve用此Serializer"""

    class Meta:
        model = Audio
        fields = "__all__"
