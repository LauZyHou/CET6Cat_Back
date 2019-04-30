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
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views

import xadmin
from xadmin.plugins import xversion

from CET6Cat.settings import MEDIA_ROOT
# from goods.views_base import GoodsListView
from goods.views import GoodsViewSet
from posts.views import PostViewSet, HotPostViewSet, ReplyViewSet
from readings.views import ReadingViewSet, HotReadingViewSet
from essays.views import EssayViewSet, HotEssayViewSet
from videos.views import VideoViewSet, HotVideoViewSet
from users.views import SmsCodeViewset, UserViewset, UserMsgViewSet, \
    PunchViewSet, UserHeadImgView, UserStudyView, UserTranslateViewSet
from favorites.views import MyWatchViewSet, WatchMeViewSet
from favorites.views import FavPostViewSet, FavVideoViewSet, FavReadingViewSet, FavEssayViewSet
from others.views import BannerViewSet, GlobalSearchViewSet, AudioViewSet, TranslateViewSet
from words.views import WordsViewSet, WordCloudViewSet, WordTrainViewSet

# XAdmin:model自动注册
xadmin.autodiscover()
xversion.register_models()

# DRF:REST风格的router
router = DefaultRouter()
router.register(r'goods', GoodsViewSet, base_name="goods")
router.register(r'posts', PostViewSet, base_name="posts")
router.register(r'readings', ReadingViewSet, base_name="readings")
router.register(r'essays', EssayViewSet, base_name="essays")
router.register(r'videos', VideoViewSet, base_name="videos")
router.register(r'code', SmsCodeViewset, base_name="code")
router.register(r'users', UserViewset, base_name="users")
router.register(r'mywatch', MyWatchViewSet, base_name="mywatch")
router.register(r'watchme', WatchMeViewSet, base_name="watchme")
router.register(r'favpost', FavPostViewSet, base_name="favpost")
router.register(r'favvideo', FavVideoViewSet, base_name="favvideo")
router.register(r'favreading', FavReadingViewSet, base_name="favreading")
router.register(r'favessay', FavEssayViewSet, base_name="favessay")
router.register(r'banners', BannerViewSet, base_name="banners")
router.register(r'usermsg', UserMsgViewSet, base_name="usermsg")
router.register(r'words', WordsViewSet, base_name="words")
router.register(r'punch', PunchViewSet, base_name="punch")
router.register(r'wordcloud', WordCloudViewSet, base_name="wordcloud")
router.register(r'hotvideo', HotVideoViewSet, base_name="hotvideo")
router.register(r'hotessay', HotEssayViewSet, base_name="hotessay")
router.register(r'hotpost', HotPostViewSet, base_name="hotpost")
router.register(r'hotreading', HotReadingViewSet, base_name="hotreading")
router.register(r'globalsearch', GlobalSearchViewSet, base_name="globalsearch")
router.register(r'reply', ReplyViewSet, base_name="reply")
router.register(r'wordtrain', WordTrainViewSet, base_name="wordtrain")
router.register(r'audios', AudioViewSet, base_name="audios")
router.register(r'translate', TranslateViewSet, base_name="translate")
# router.register(r'userheadimg', UserHeadImgView.as_view(), base_name="userheadimg")
router.register(r'usertranslate', UserTranslateViewSet, base_name="usertranslate")

urlpatterns = [
    path('', include(router.urls)),
    path('xadmin/', xadmin.site.urls),
    # path('goods/', GoodsListView.as_view(), name="goods-list"),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找,使用配置好的路径
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 自动化文档,1.11版本中注意此处前往不要加$符号
    path('docs/', include_docs_urls(title="CET6Cat文档")),
    # DRF调试登录,配置了这个才会有登录按钮
    path('api-auth/', include('rest_framework.urls')),
    # drf自带的token授权登录,获取token需要向该地址post数据(username和password)
    path('api-token-auth/', views.obtain_auth_token),
    # jwt的token认证,现在改用这个而不用上面那个drf自带的了
    path('login/', obtain_jwt_token),
    # 上传用户头像
    path('userheadimg/', UserHeadImgView.as_view()),
    # 获取学习情况
    path('userstudy/', UserStudyView.as_view())
]
