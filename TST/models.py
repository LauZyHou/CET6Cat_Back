from django.db import models

"""
仅供测试用!
"""


class User(models.Model):
    """用户信息"""
    user_name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    def __unicode__(self):
        return self.user_name
