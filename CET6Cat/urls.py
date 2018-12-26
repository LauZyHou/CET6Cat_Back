"""CET6Cat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import UNIVERSAL.views
# 每个APP里自己定义的urls.py文件都要导入到这里
import USR_MSG.urls

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'index/', UNIVERSAL.views.index),
    path(r'gosub/', UNIVERSAL.views.gosub),
    path(r'um/', include(USR_MSG.urls))
]
