from django.db.models.signals import pre_delete
from django.dispatch import receiver

from posts.models import Post
from db_tools.redis_pool import RedisPool


@receiver(pre_delete, sender=Post)
def delete_post_key_in_redis(sender, instance=None, created=False, **kwargs):
    """Post对象删除前触发"""
    # 删除redis中的key
    pid = getattr(instance, 'id', '')
    r = RedisPool.get_connection()
    r.delete("post_" + str(pid))
