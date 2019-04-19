import xadmin
from others.models import Banner, Audio, Translate


class BannerAdmin(object):
    """轮播图"""
    list_display = ["name", "path", "index"]


class AudioAdmin(object):
    """听力资源"""
    list_display = ["name", "content", "exam", "answer", "add_time"]


class TranslateAdmin(object):
    """翻译资源"""
    list_display = ["name", "exam", "answer", "add_time"]


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Audio, AudioAdmin)
xadmin.site.register(Translate, TranslateAdmin)
