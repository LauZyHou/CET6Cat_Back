from django.db.models.signals import pre_delete
from django.dispatch import receiver

from readings.models import Reading


@receiver(pre_delete, sender=Reading)
def delete_reading_files(sender, instance=None, created=False, **kwargs):
    """Reading对象删除前触发"""
    reading = getattr(instance, 'content', '')  # <class 'django.db.models.fields.files.FieldFile'>
    # 删除文件
    reading.delete(save=False)
