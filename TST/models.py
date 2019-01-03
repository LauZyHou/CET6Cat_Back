from django.db import models
from django.contrib.auth.models import AbstractUser

"""
仅供测试用!
"""


class User(AbstractUser):
    """用户信息"""
    # user_name = models.CharField(max_length=32, default="Flora")
    # password = models.CharField(max_length=32)
    # REQUIRED_FIELDS = ['user_name']

    # 元数据
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
