from rest_framework import serializers

from words.models import Word


class WordSerializer(serializers.ModelSerializer):
    """单词使用这个Serializer"""

    class Meta:
        model = Word
        fields = "__all__"
