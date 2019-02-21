import xadmin
from favorites.models import Watch, FavEssay, FavPost, FavReading, FavVideo


class WatchAdmin(object):
    """关注"""
    list_display = ["base", "uper"]


class FavEssayAdmin(object):
    """收藏作文"""
    list_display = ["base", "uper"]


class FavPostAdmin(object):
    """收藏帖子"""
    list_display = ["base", "uper"]


class FavReadingAdmin(object):
    """收藏文章"""
    list_display = ["base", "uper"]


class FavVideoAdmin(object):
    """收藏视频"""
    list_display = ["base", "uper"]


xadmin.site.register(Watch, WatchAdmin)
xadmin.site.register(FavEssay, FavEssayAdmin)
xadmin.site.register(FavPost, FavPostAdmin)
xadmin.site.register(FavReading, FavReadingAdmin)
xadmin.site.register(FavVideo, FavVideoAdmin)

