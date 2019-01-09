from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

"""
仅供测试用!
"""


class User(AbstractBaseUser):
    """用户信息"""
    username = models.CharField(max_length=20)
    # password = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)

    def check_password(self):
        # return self.password == '111111'
        return True
