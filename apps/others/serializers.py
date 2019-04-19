from rest_framework import serializers

from others.models import Banner, Audio, Translate


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


class TranslateSerializer(serializers.ModelSerializer):
    """翻译list用此Serializer"""

    class Meta:
        model = Translate
        fields = ("id", "name")


class TranslateDetailSerializer(serializers.ModelSerializer):
    """翻译retrieve用此Serializer"""

    class Meta:
        model = Translate
        fields = "__all__"
