import xadmin

from readings.models import Site
from readings.models import Reading


class SiteAdmin(object):
    """外部站点"""
    list_display = ["name", "url"]


class ReadingAdmin(object):
    """文章"""
    list_display = ["name", "source", "add_time"]


xadmin.site.register(Site, SiteAdmin)
xadmin.site.register(Reading, ReadingAdmin)
