import xadmin
from xadmin import views

from videos.models import Video


class VideoAdmin(object):
    """视频"""
    list_display = ["name", "uper", "add_time"]


xadmin.site.register(Video, VideoAdmin)
