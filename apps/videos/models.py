from django.db import models
from datetime import datetime

from users.models import UserProfile


class Video(models.Model):
    """视频"""
    CATEGORY_CHOICE = (
        (1, "课程"),
        (2, "考试"),
        (3, "综合"),
        (4, "娱乐")
    )
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name="视频名称")
    content = models.FileField(upload_to="videos/", null=True, blank=True, verbose_name="视频内容")
    thumb = models.ImageField(upload_to="video_thumb/", null=True, blank=True, verbose_name="缩略图")
    category = models.IntegerField(choices=CATEGORY_CHOICE, default=1, verbose_name="视频类别")
    uper = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="上传者", related_name="videos")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    hot_value = models.IntegerField(default=0, verbose_name="热度指数")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = "视频们"

    def __str__(self):
        return self.name
