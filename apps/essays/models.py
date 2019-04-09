from django.db import models
from datetime import datetime


class Essay(models.Model):
    """作文"""
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="作文标题")
    content = models.FileField(upload_to="essays/", null=True, blank=True, verbose_name="作文内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    hot_value = models.IntegerField(default=0, verbose_name="热度指数")

    class Meta:
        verbose_name = "作文"
        verbose_name_plural = "作文们"

    def __str__(self):
        return self.name
