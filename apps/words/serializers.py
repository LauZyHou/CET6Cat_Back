from rest_framework import serializers

from words.models import Word


class WordSerializer(serializers.ModelSerializer):
    """单词使用这个Serializer"""

    class Meta:
        model = Word
        fields = "__all__"


class WordCloudSerializer(serializers.ModelSerializer):
    """词云使用这个Serializer"""

    class Meta:
        model = Word
        fields = ("id", "name")  # todo nums


class WordTrainSerializer(serializers.ModelSerializer):
    """专项训练->单词测验->组卷用这个Serializer"""

    class Meta:
        model = Word
        fields = ("id", "name", "explain")
