from rest_framework import serializers

from posts.models import Post, Reply
from users.models import UserProfile


class UperSerializer(serializers.ModelSerializer):
    """用户Serializer,用于展示帖子中可见的用户视图"""

    class Meta:
        model = UserProfile
        fields = ("id", "username", "gender", "head_img")


class ReplySerializer(serializers.ModelSerializer):
    """回帖Serializer,用于帖子详情"""

    # 用户仅展示部分信息,但不止是id
    uper = UperSerializer()

    class Meta:
        model = Reply
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    """帖子list用这个Serializer"""

    # 带上它自己的回帖,注意在Models中定义related_name="replies"
    replies = ReplySerializer(many=True)
    uper = UperSerializer()

    # list接口不带content
    class Meta:
        model = Post
        fields = ("id", "name", "category", "add_time", "uper", "replies")
        # depth = 1


class PostDetailSerializer(serializers.ModelSerializer):
    """帖子retrieve用这个Serializer"""

    replies = ReplySerializer(many=True)
    uper = UperSerializer()

    class Meta:
        model = Post
        fields = "__all__"
