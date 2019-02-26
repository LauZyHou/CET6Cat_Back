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
from django.views.static import serve
from django.urls import path, re_path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

import xadmin
from xadmin.plugins import xversion

from CET6Cat.settings import MEDIA_ROOT
# from goods.views_base import GoodsListView
from goods.views import GoodsViewSet
from posts.views import PostViewSet
from readings.views import ReadingViewSet
from essays.views import EssayViewSet

# XAdmin:model自动注册
xadmin.autodiscover()
xversion.register_models()

# DRF:REST风格的router
router = DefaultRouter()
router.register(r'goods', GoodsViewSet, base_name="goods")
router.register(r'posts', PostViewSet, base_name="posts")
router.register(r'readings', ReadingViewSet, base_name="readings")
router.register(r'essays', EssayViewSet, base_name="essays")

urlpatterns = [
    path('', include(router.urls)),
    path('xadmin/', xadmin.site.urls),
    # path('goods/', GoodsListView.as_view(), name="goods-list"),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找,使用配置好的路径
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]
