from django.db.models.signals import pre_delete
from django.dispatch import receiver

from essays.models import Essay


@receiver(pre_delete, sender=Essay)
def delete_reading_files(sender, instance=None, created=False, **kwargs):
    """Essay对象删除前触发"""
    essay = getattr(instance, 'content', '')  # <class 'django.db.models.fields.files.FieldFile'>
    # 删除文件
    essay.delete(save=False)
