from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """用户(由手机号标识)"""
    GENDER_CHOICES = (
        (True, "男"),
        (False, "女")
    )
    # 用户注册时用的是mobile,没提供name之类的信息,所以可以为null
    # 注意null针对数据库,blank针对表单
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name="昵称")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    gender = models.BooleanField(choices=GENDER_CHOICES, default=True, verbose_name="性别")
    # 这里如果设置成不允许为null,那么在用户注册的Serializer里因为用了ModelSerializer,就要求mobile是必填的
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话", help_text="中国内地")
    email = models.EmailField(max_length=40, null=True, blank=True, verbose_name="邮箱")
    college = models.CharField(max_length=30, null=True, blank=True, verbose_name="大学")
    catb = models.IntegerField(default=0, verbose_name="Cat币")
    brief = models.CharField(max_length=100, null=True, blank=True, verbose_name="个人简介")
    head_img = models.ImageField(upload_to="user_head/", null=True, blank=True, verbose_name="用户头像")
    switch_sec = models.IntegerField(default=4, verbose_name="单词切换间隔")
    email_notice = models.BooleanField(default=True, verbose_name="开启邮箱通知")
    # 打卡时,当前日期==last_punch+1则视为连续打卡.某次打卡时判断出打卡中断则conti_punch=0
    conti_punch = models.IntegerField(default=0, verbose_name="最近连续打卡")
    last_punch = models.DateField(null=True, blank=True, verbose_name="最后打卡日期")
    # 背单词进度和当前背到第几组由words_num计算
    words_num = models.IntegerField(default=1, verbose_name="当前背到的单词")
    vip = models.IntegerField(default=0, verbose_name="VIP等级")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户们"

    # py2里才有string转Unicode,py3里默认都是Unicode,直接用__str__()
    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    验证码(由手机号关联,回填验证码进行验证,可以考虑保存在redis中)
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = "验证码们"

    def __str__(self):
        return self.code
