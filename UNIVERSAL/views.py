from django.shortcuts import render
from django.shortcuts import HttpResponse
import USR_MSG.models


# Create your views here.

def index(request):
    input_dict_lst = USR_MSG.models.UserLogin.objects.all()
    # 返回HTML页面时,使用render来渲染和打包
    return render(request, 'universal/index.html', {'list': input_dict_lst})


# 表单提交调用的函数
def gosub(request):
    # 相当于Java的Servlet中的doPost情况
    if request.method == 'POST':
        # 获取表单提交来的数据
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # 在控制台输出表单的提交看一下
        print(username, password)
        # 将这些数据添加到数据库
        USR_MSG.models.UserLogin.objects.create(user_name=username, password=password)
    # 从数据库中读取所有数据
    input_dict_lst = USR_MSG.models.UserLogin.objects.all()
    # 返回一个页面,如返回自己这个页面本身,第三个参数以字典方式提供数据对象
    return render(request, 'universal/index.html', {'list': input_dict_lst})
