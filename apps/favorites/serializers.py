from rest_framework import serializers
from favorites.models import Watch, FavPost, FavVideo, FavReading, FavEssay
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Post
from videos.models import Video
from readings.models import Reading
from users.models import UserProfile
from essays.models import Essay


# ---------------------------------[临时Serializer]-----------------------------------------

class UserProfileSerializer(serializers.ModelSerializer):
    """用于[MyWatchDetailSerializer/WatchMeDetailSerializer]的用户(被关注者/关注者)序列化类"""

    class Meta:
        model = UserProfile
        fields = ("id", "name")  # "gender"和"head_img"被去掉了,简洁一些


class PostSerializer(serializers.ModelSerializer):
    """专用于[FavPostDetailSerializer]的帖子序列化类"""

    class Meta:
        model = Post
        fields = ("id", "name")


class VideoSerializer(serializers.ModelSerializer):
    """专用于[FavVideoDetailSerializer]的视频序列化类"""

    class Meta:
        model = Video
        fields = ("id", "name")


class ReadingSerializer(serializers.ModelSerializer):
    """专用于[FavReadingDetailSerializer]的文章序列化类"""

    class Meta:
        model = Reading
        fields = ("id", "name")


class EssaySerializer(serializers.ModelSerializer):
    """专用于[FavEssayDetailSerializer]的作文序列化类"""

    class Meta:
        model = Essay
        fields = ("id", "name")


# ---------------------------------[我关注的人]-----------------------------------------


class MyWatchSerializer(serializers.ModelSerializer):
    """我关注的人 >>create,destroy"""
    # 用户收藏时不指明用户,只操作自己这个用户
    uper = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # 设置read_only只返回(用于持久化 & 返回给前端),不在用户提交时要求用户提供
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    def validate(self, attrs):
        """验证,禁止用户关注自己"""
        if attrs["base"] == attrs["uper"]:
            raise serializers.ValidationError("不能关注自己")
        return attrs

    class Meta:
        model = Watch
        # 实现唯一联合,不允许重复收藏,在Model级别也做了
        validators = [
            UniqueTogetherValidator(
                queryset=Watch.objects.all(),
                fields=('base', 'uper'),
                message="您已关注过该用户"
            )
        ]
        fields = ("base", "uper", "add_time")


class MyWatchDetailSerializer(serializers.ModelSerializer):
    """我关注的人(被关注者详细) >>list"""

    # 覆盖掉之前仅仅是UserProfile的id的base字段
    base = UserProfileSerializer()

    class Meta:
        model = Watch
        # 删除时直接提供要删除的用户id即可,所以这里不再需要返回Watch表的id
        fields = ("base",)


# ---------------------------------[关注我的人]-----------------------------------------

class WatchMeDetailSerializer(serializers.ModelSerializer):
    """关注我的人(关注者详细) >>list"""

    # 覆盖掉之前仅仅是UserProfile的id的uper字段
    uper = UserProfileSerializer()

    class Meta:
        model = Watch
        fields = ("uper",)


# ---------------------------------[我收藏的帖子]-----------------------------------------

class FavPostSerializer(serializers.ModelSerializer):
    """我收藏的帖子 >>create,destroy"""

    # 用户收藏时不指明用户,只操作"我"这个用户
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
    """我收藏的帖子(帖子详细) >>list"""

    # 不需要再用隐藏字段指明uper,因为该字段仅用于list视图,不存在create时需要知道uper是谁的问题
    # 在FavPostViewSet中已经只返回了本用户的数据

    # 覆盖掉之前仅仅是Post的id的base字段
    base = PostSerializer()

    class Meta:
        model = FavPost
        fields = ("id", "base", "add_time")  # 这里id将被返回给前端,这样在destroy时前端才能提供id


# ---------------------------------[我收藏的视频]-----------------------------------------

class FavVideoSerializer(serializers.ModelSerializer):
    """我收藏的视频 >>create,destroy"""
    uper = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = FavVideo
        validators = [
            UniqueTogetherValidator(
                queryset=FavVideo.objects.all(),
                fields=('base', 'uper'),
                message="视频已经收藏"
            )
        ]
        fields = ("base", "uper", "add_time")


class FavVideoDetailSerializer(serializers.ModelSerializer):
    """我收藏的视频(视频详细) >>list"""
    base = VideoSerializer()

    class Meta:
        model = FavVideo
        fields = ("id", "base", "add_time")


# ---------------------------------[我收藏的文章]-----------------------------------------

class FavReadingSerializer(serializers.ModelSerializer):
    """我收藏的文章 >>create,destroy"""
    uper = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = FavReading
        validators = [
            UniqueTogetherValidator(
                queryset=FavReading.objects.all(),
                fields=('base', 'uper'),
                message="文章已经收藏"
            )
        ]
        fields = ("base", "uper", "add_time")


class FavReadingDetailSerializer(serializers.ModelSerializer):
    """我收藏的文章(文章详细) >>list"""
    base = ReadingSerializer()

    class Meta:
        model = FavReading
        fields = ("id", "base", "add_time")


# ---------------------------------[我收藏的作文]-----------------------------------------

class FavEssaySerializer(serializers.ModelSerializer):
    """我收藏的作文 >>create,destroy"""
    uper = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = FavEssay
        validators = [
            UniqueTogetherValidator(
                queryset=FavEssay.objects.all(),
                fields=('base', 'uper'),
                message="作文已经收藏"
            )
        ]
        fields = ("base", "uper", "add_time")


class FavEssayDetailSerializer(serializers.ModelSerializer):
    """我收藏的作文(作文详细) >>list"""
    base = EssaySerializer()

    class Meta:
        model = FavEssay
        fields = ("id", "base", "add_time")

# ---------------------------------[]-----------------------------------------
