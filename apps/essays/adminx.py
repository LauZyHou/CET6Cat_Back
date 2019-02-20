import xadmin

from essays.models import Essay


class EssayAdmin(object):
    """作文"""
    list_display = ["name", "add_time"]


xadmin.site.register(Essay, EssayAdmin)
