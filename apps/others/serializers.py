from rest_framework import serializers

from others.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    """轮播图Serializer"""

    class Meta:
        model = Banner
        fields = "__all__"
