from django.db import models
from datetime import datetime


class Site(models.Model):
    """外部站点(用于文章来源)"""
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name="站点名称")
    url = models.URLField(null=True, blank=True, verbose_name="URL")

    class Meta:
        verbose_name = "外部站点"
        verbose_name_plural = "外部站点们"

    def __str__(self):
        return self.name


class Reading(models.Model):
    """文章"""
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="文章标题")
    content = models.FileField(upload_to="readings/", null=True, blank=True, verbose_name="文章内容")
    source = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name="来源", related_name="readings")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    hot_value = models.IntegerField(default=0, verbose_name="热度指数")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章们"

    def __str__(self):
        return self.name
