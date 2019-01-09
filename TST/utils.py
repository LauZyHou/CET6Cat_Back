from django.contrib.auth.backends import ModelBackend
from TST.models import User
import re


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_account(account):
    """判断用户登陆的是用户名还是手机号"""
    try:
        if re.match('^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    # FIXME exceptions must derive from BaseException
    except User.DoesNotExist:
        raise None
    return user


# 自定义Ｄｊａｎｇｏ的认证，满足多账号的登陆
class UsernameMobileAuthBackend(ModelBackend):
    """对用户进行密码身份的校验"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_account(username)
        print(user.username,user.password)
        if user is not None and user.check_password():
            """如果用户密码校验成功，返回用户模型对象，当然了，如果用户不存在，那么就不用再返回None了，因为在调用函数的时候
            就返回None"""
            return user
