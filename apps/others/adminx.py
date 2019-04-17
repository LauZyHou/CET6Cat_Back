import xadmin
from others.models import Banner, Audio


class BannerAdmin(object):
    """轮播图"""
    list_display = ["name", "path", "index"]


class AudioAdmin(object):
    """听力资源"""
    list_display = ["name", "content", "add_time"]


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Audio, AudioAdmin)
