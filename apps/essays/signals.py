from django.db.models.signals import pre_delete
from django.dispatch import receiver

from essays.models import Essay
from db_tools.redis_pool import RedisPool


@receiver(pre_delete, sender=Essay)
def delete_reading_files(sender, instance=None, created=False, **kwargs):
    """Essay对象删除前触发"""
    # 删除文件
    essay = getattr(instance, 'content', '')  # <class 'django.db.models.fields.files.FieldFile'>
    essay.delete(save=False)
    # 删除redis中的key
    eid = getattr(instance, 'id', '')
    r = RedisPool.get_connection()
    r.delete("essay_" + str(eid))
