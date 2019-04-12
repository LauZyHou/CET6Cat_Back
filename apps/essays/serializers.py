from rest_framework import serializers

from essays.models import Essay


class EssaySerializer(serializers.ModelSerializer):
    """作文list用这个Serializer"""

    # 不带内容content
    class Meta:
        model = Essay
        fields = ("id", "name", "add_time")


class EssayDetailSerializer(serializers.ModelSerializer):
    """作文retrieve用这个Serializer"""

    class Meta:
        model = Essay
        fields = "__all__"


class HotEssaySerializer(serializers.ModelSerializer):
    """热门作文list用这个Serializer"""

    class Meta:
        model = Essay
        fields = ("id", "name", "add_time", "hot_value")
