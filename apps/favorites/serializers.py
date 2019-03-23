from rest_framework import serializers
from favorites.models import Watch, FavPost, FavVideo, FavReading, FavEssay
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Post


# ------------------------------------------------------------------------------------

class PostSerializer(serializers.ModelSerializer):
    """专用于[FavPostDetailSerializer]的帖子序列化类"""

    class Meta:
        model = Post
        fields = ("id", "name")


class FavPostSerializer(serializers.ModelSerializer):
    """收藏帖子"""

    # 用户收藏时不指明用户,只操作自己这个用户
    uper = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # 设置read_only只返回(用于持久化 & 返回给前端),不在用户提交时要求用户提供
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = FavPost
        # 实现唯一联合,不允许重复收藏,在Model级别也做了
        validators = [
            UniqueTogetherValidator(
                queryset=FavPost.objects.all(),
                fields=('base', 'uper'),
                message="帖子已经收藏"
            )
        ]
        fields = ("base", "uper", "add_time")


class FavPostDetailSerializer(serializers.ModelSerializer):
    """收藏帖子（帖子详细）"""

    # 不需要再用隐藏字段指明uper,因为该字段仅用于list视图,不存在create时需要知道uper是谁的问题
    # 在FavPostViewSet中已经只返回了本用户的数据

    # 覆盖掉之前仅仅是Post的id的base字段
    base = PostSerializer()

    class Meta:
        model = FavPost
        fields = ("id", "base")  # 这里id将被返回给前端,这样在destroy时前端才能提供id
