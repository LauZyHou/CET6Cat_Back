from rest_framework import serializers

from posts.models import Post, Reply
from users.models import UserProfile


class UperSerializer(serializers.ModelSerializer):
    """用户Serializer,用于展示帖子详情中可见的用户视图"""

    class Meta:
        model = UserProfile
        fields = ("id", "name", "gender", "head_img")


class Uper2NameSerializer(serializers.ModelSerializer):
    """Uper转其Name字段,用于帖子list"""

    class Meta:
        model = UserProfile
        fields = ("name",)


class ReplySerializer(serializers.ModelSerializer):
    """回帖Serializer,用于帖子详情"""

    # 用户仅展示部分信息,但不止是id
    uper = UperSerializer()

    class Meta:
        model = Reply
        fields = "__all__"


class SimpleReplySerializer(serializers.ModelSerializer):
    """极简的回帖Serializer,用于帖子list"""

    # 仅用户昵称
    uper = Uper2NameSerializer()

    class Meta:
        model = Reply
        # [重大改动]此处优化性能,仅仅返回uper字段(uper也只有name)和添加时间(用于展示最后修改时间)
        fields = ("uper", "add_time")


class PostSerializer(serializers.ModelSerializer):
    """帖子list用这个Serializer"""

    # 带上它自己的回帖,注意在Models中定义related_name="replies"
    replies = SimpleReplySerializer(many=True)
    uper = Uper2NameSerializer()

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


class PostAddSerializer(serializers.ModelSerializer):
    """帖子create用这个Serializer"""

    class Meta:
        model = Post
        fields = "__all__"


class HotPostSerializer(serializers.ModelSerializer):
    """热门帖子list用这个Serializer"""

    class Meta:
        model = Post
        fields = ("id", "name", "category", "add_time", "uper", "hot_value")


class ReplyDetailSerializer(serializers.ModelSerializer):
    """用于创建回帖的Serializer"""

    class Meta:
        model = Reply
        fields = "__all__"
