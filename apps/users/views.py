from random import choice

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# 用于生成payload然后生成token
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework.response import Response
from rest_framework import mixins, permissions, authentication
from rest_framework import viewsets, status

from utils.yunpian import YunPian
from users.models import VerifyCode, UserProfile
from users.serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from CET6Cat.privacy import YUNPIAN_KEY


class CustomBackend(ModelBackend):
    """
    自定义用户验证规则:对用户名和手机号都可以验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    点击发送短信验证码时向此view请求
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码字符串
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        """生成验证码,调用云片接口发送,并将验证码保存到数据库"""
        # 验证mobile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 这里验证失败会raise一个ValidationError而不执行后面的
        mobile = serializer.validated_data["mobile"]  # 取出通过验证的mobile
        # 生成验证码
        code = self.generate_code()
        """
        # 云片网发送短信
        yun_pian = YunPian(YUNPIAN_KEY)
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        # 发送失败
        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]  # 这里将云片网发送短信接口的错误信息放到mobile字段了
            }, status=status.HTTP_400_BAD_REQUEST)  # 遵循REST规范,用HTTP状态码表征请求的结果如何
        # 发送成功
        else:
        """
        code_record = VerifyCode(code=code, mobile=mobile)  # 验证码,手机号对应
        code_record.save()  # 保存到数据库
        return Response({
            "mobile": mobile
        }, status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    用户create,update,retrieve时向此view请求
    """
    queryset = UserProfile.objects.all()
    # 用户认证(普通用户从CET6Cat登录用的是JWT,管理员用户从XAdmin登录用的是Session)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # 如果用permission_classes定义访问权限认证IsAuthenticated已登录(否则401)
    # 那么对这个整个用户视图都生效,但用户在注册时肯定不能在"已登录"状态下
    # 所以将permission以动态的方式定义
    def get_permissions(self):
        """覆写,以在不同的请求方法下使用不同的权限认证"""
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]  # 在已登录的状态下才能访问retrieve(访问自己的信息)
        elif self.action == "create":
            return [permissions.AllowAny()]  # 登录/没登录都允许
        return []  # 使用空数组也和仅有AllowAny()一样的

    def create(self, request, *args, **kwargs):
        """
        用户注册(注意username填写手机号)
        覆写,以将token加入response给用户(实现注册完自动登录)
        """
        serializer = self.get_serializer(data=request.data)
        # Serializer中做验证并可能抛出异常,出错时将自动返回相应的HTTP状态码
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """覆写,将user返回以在create里能取到"""
        return serializer.save()

    # 该方法在GET(retrieve)和DELETE(destroy)和PUT(update)时都调用,但对用户而言仅应能操作自己这个用户
    def get_object(self):
        """覆写,不管传什么id,都只返回当前用户"""
        return self.request.user

    def get_serializer_class(self):
        """覆写,在不同的请求下做不同的序列化"""
        if self.action == "retrieve":
            return UserDetailSerializer  # 用户详情用
        elif self.action == "create":
            return UserRegSerializer  # 用户注册用
        return UserDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        """获取本用户信息(需身份验证,id无论提供多少,仅返回本用户的信息)"""
        return super().retrieve(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        """更新本用户信息(需身份验证,id无论提供多少,仅更新本用户的信息)"""
        return super().update(request, args, kwargs)

    def partial_update(self, request, *args, **kwargs):
        """部分更新,只更新提供的字段(需身份验证,id无论提供多少,仅更新本用户的信息)"""
        kwargs['partial'] = True
        # 因为用户名是必填项目,在部分更新时为了不要求提供,直接从authorization中取用
        if "username" not in request.data.keys():
            request.data.update({"username": self.request.user.username})
        return self.update(request, *args, **kwargs)
