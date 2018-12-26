from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from USR_MSG.models import User
from django.core import serializers

try:
    import ujson as json
except ImportError:
    import json


# Create your views here.

@require_http_methods(['GET'])
def add_user(request):
    """添加用户"""
    response = {}
    try:
        user = User(user_name=request.GET.get('user_name'))
        user.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def get_users(request):
    """获取用户信息"""
    response = {}
    try:
        users = User.objects.filter()
        # 注意区分:json.loads()函数是将json格式数据转换为字典,json.load()用来读json文件
        response['list'] = json.loads(serializers.serialize("json", users))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
