from django.db.models.signals import pre_delete
from django.dispatch import receiver

from readings.models import Reading
from db_tools.redis_pool import RedisPool


@receiver(pre_delete, sender=Reading)
def delete_reading_files(sender, instance=None, created=False, **kwargs):
    """Reading对象删除前触发"""
    # 删除文件
    reading = getattr(instance, 'content', '')  # <class 'django.db.models.fields.files.FieldFile'>
    reading.delete(save=False)
    # 删除redis中的key
    rid = getattr(instance, 'id', '')
    r = RedisPool.get_connection()
    r.delete("reading_" + str(rid))
