from rest_framework.validators import UniqueValidator

import re
from datetime import datetime, timedelta
from users.models import VerifyCode
from rest_framework import serializers

from users.models import UserProfile
from favorites.models import Watch
from CET6Cat.settings import REGEX_MOBILE


class SmsSerializer(serializers.Serializer):
    """获取验证码用此Serializer"""
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码(函数名称必须为validate_ + 字段名)
        """
        # 手机是否注册
        if UserProfile.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 数据库中存在添加时间大于一分钟以前的本mobile的验证码。也就是距离现在还不足一分钟
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """用户create(注册)用此Serializer"""
    # 验证码code只用来做验证,不必再返回给用户,所以设置write_only=True
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",  # 这个字段有传过来,但是为空
                                     "required": "请输入验证码",  # 这个字段没有传过来
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")

    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message="用户已经存在")])
    # 如果前端POST验证成功,这里序列化成功就会把序列化的字段返回给前端,这里不希望password被返回所以设置write_only
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    # 调用父类的create方法，该方法会返回当前model的实例化对象即user。
    # 前面是将父类原有的create进行执行，后面是加入自己的逻辑
    # def create(self, validated_data):
    #     """覆写create以实现密码单独设置,因为ModelSerializer会把它明文保存"""
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user
    """改为用信号量实现"""

    def validate_code(self, code):

        # get与filter的区别: get有两种异常，一个是有多个，一个是一个都没有。
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # 验证码在数据库中是否存在，用户从前端post过来的值都会放入initial_data里面，排序(最新一条)。
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        print(verify_records)
        if verify_records:
            # 获取到最新一条
            last_record = verify_records[0]

            # 有效期为五分钟。
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码不存在")

    # 不加字段名的验证器作用于所有字段之上。attrs是字段 validate之后返回的总的dict
    def validate(self, attrs):
        # 这里本来将电话号码放到username里作为用户初始的用户名,这里在验证完之后把它放到用户的mobile字段里(本来就应该放在这里
        attrs["mobile"] = attrs["username"]
        # 因为code字段不在UserProfile里,只是用来验证的,所以验证完就把它删掉
        del attrs["code"]
        return attrs

    class Meta:
        model = UserProfile
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户retrieve自己,用此Serializer(给详细信息)
    """

    class Meta:
        model = UserProfile
        fields = ("id", "username", "name", "birthday", "gender", "mobile",
                  "email", "college", "catb", "brief", "head_img",
                  "switch_sec", "email_notice", "conti_punch", "last_punch",
                  "words_num", "vip")


class UserMsgSerializer(serializers.ModelSerializer):
    """
    用户retrieve任意用户,用此Serializer(只给简要信息)
    """

    class Meta:
        model = UserProfile
        fields = ("id", "name", "gender", "college", "brief", "head_img",
                  "conti_punch", "words_num", "vip")


class PunchSerializer(serializers.ModelSerializer):
    """
    用户打卡时使用该视图
    """
    # 这两个字段只读(只返回给用户看,不用于写入)
    name = serializers.CharField(read_only=True)
    head_img = serializers.ImageField(read_only=True)

    # conti_punch和last_punch在View中设置
    # words_num由前台传过来

    class Meta:
        model = UserProfile
        fields = ("name", "head_img", "conti_punch", "last_punch", "words_num")


class GroupSerializer(serializers.ModelSerializer):
    """
    用户获取组号时使用该视图
    """

    class Meta:
        model = UserProfile
        fields = ("words_num",)
