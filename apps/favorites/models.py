from django.db import models
from datetime import datetime

from users.models import UserProfile
from posts.models import Post
from videos.models import Video
from readings.models import Reading
from essays.models import Essay


class Watch(models.Model):
    """关注"""
    # 在一个表中多次引用某个外键表,要指定唯一的releated_name
    base = models.ForeignKey(UserProfile, related_name="to_user", on_delete=models.CASCADE, verbose_name="被关注者")
    uper = models.ForeignKey(UserProfile, related_name="from_user", on_delete=models.CASCADE, verbose_name="关注者")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="关注时间")

    class Meta:
        verbose_name = "关注"
        verbose_name_plural = "关注们"
        unique_together = ("base", "uper")

    def __str__(self):
        return self.base.username + "<-" + self.uper.username


class FavPost(models.Model):
    """收藏帖子"""
    base = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="被收藏贴")
    uper = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="收藏者")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "收藏帖子"
        verbose_name_plural = "收藏帖子们"
        unique_together = ("base", "uper")

    def __str__(self):
        return self.base.name + "<-" + self.uper.username


class FavVideo(models.Model):
    """收藏视频"""
    base = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="被收藏视频")
    uper = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="收藏者")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "收藏视频"
        verbose_name_plural = "收藏视频们"
        unique_together = ("base", "uper")

    def __str__(self):
        return self.base.name + "<-" + self.uper.username


class FavReading(models.Model):
    """收藏文章"""
    base = models.ForeignKey(Reading, on_delete=models.CASCADE, verbose_name="被收藏文章")
    uper = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="收藏者")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "收藏文章"
        verbose_name_plural = "收藏文章们"
        unique_together = ("base", "uper")

    def __str__(self):
        return self.base.name + "<-" + self.uper.username


class FavEssay(models.Model):
    """收藏作文"""
    base = models.ForeignKey(Essay, on_delete=models.CASCADE, verbose_name="被收藏作文")
    uper = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="收藏者")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "收藏作文"
        verbose_name_plural = "收藏作文们"
        unique_together = ("base", "uper")

    def __str__(self):
        return self.base.name + "<-" + self.uper.username
