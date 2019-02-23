from django.db import models
from datetime import datetime


# Create your models here.

class Banner(models.Model):
    """首页轮播图"""
    name = models.CharField(max_length=20, verbose_name="描述")
    path = models.CharField(max_length=10, verbose_name="路由")  # 定位到站内的任意资源
    img = models.ImageField(upload_to="banner/", verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "首页轮播图"
        verbose_name_plural = "首页轮播图们"

    def __str__(self):
        return self.name
