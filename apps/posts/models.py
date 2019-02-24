from django.db import models
from datetime import datetime

from users.models import UserProfile


class Post(models.Model):
    """帖子"""
    CATEGORY_CHOICE = (
        (1, "求助"),
        (2, "分享"),
        (3, "综合"),
        (4, "闲聊"),
    )
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="帖子标题")
    content = models.CharField(max_length=200, null=True, blank=True, verbose_name="帖子内容")
    category = models.IntegerField(choices=CATEGORY_CHOICE, default=1, verbose_name="帖子类别")
    uper = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="发帖人")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发帖时间")

    class Meta:
        verbose_name = "帖子"
        verbose_name_plural = "帖子们"

    def __str__(self):
        return self.name


class Reply(models.Model):
    """回帖"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="基帖", related_name="replies")
    content = models.CharField(max_length=100, null=True, blank=True, verbose_name="回帖内容")
    uper = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="回帖人")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="回帖时间")

    class Meta:
        verbose_name = "回帖"
        verbose_name_plural = "回帖们"

    def __str__(self):
        return "Re:" + self.post.name
