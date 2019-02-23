import xadmin
from others.models import Banner


class BannerAdmin(object):
    """轮播图"""
    list_display = ["name", "path", "index"]


xadmin.site.register(Banner, BannerAdmin)
