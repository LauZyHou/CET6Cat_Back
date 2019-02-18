import xadmin
from posts.models import Post, Reply


class PostAdmin(object):
    """帖子"""
    list_display = ["name", "category", "uper", "add_time"]


class ReplyAdmin(object):
    """回帖"""
    list_display = ["post", "content", "uper", "add_time"]


xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Reply, ReplyAdmin)
