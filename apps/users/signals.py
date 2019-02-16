"""
注意在app.js中要在ready中导入本文件

各种信号量见:
https://www.cnblogs.com/renpingsheng/p/7566647.html
"""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()


# 参数一接收哪种信号，参数二是接收哪个model的信号
@receiver(post_save, sender=User)
def create_user_password(sender, instance=None, created=False, **kwargs):
    """User对象保存后自动触发"""
    # 是否新建，因为update的时候也会进行post_save
    # 这里只有在新建的时候才去把password从明文该成密文再存到数据库里
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()  # 注意这个save又会触发post_save,但已经不满足created==True了
