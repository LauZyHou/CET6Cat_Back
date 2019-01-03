from rest_framework import serializers
# from TST.models import VerifyCode


class VerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        # model = VerifyCode
        fields = "__all__"
