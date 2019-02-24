from rest_framework import serializers

from posts.models import Post, Reply


class ReplySerializer(serializers.ModelSerializer):
    """回帖Serializer,用于帖子详情"""

    class Meta:
        model = Reply
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    """帖子list用这个Serializer"""

    # Post本身的所有字段,不带回帖
    class Meta:
        model = Post
        fields = "__all__"


class PostDetailSerializer(serializers.ModelSerializer):
    """帖子retrieve用这个Serializer"""

    # 带上它自己的回帖,注意在Models中定义related_name="replies"
    replies = ReplySerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
