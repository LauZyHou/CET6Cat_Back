from django.db import models


# Create your models here.

class UserLogin(models.Model):
    """用户登录信息"""
    user_name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
