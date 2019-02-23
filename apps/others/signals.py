from django.db.models.signals import pre_delete
from django.dispatch import receiver

from others.models import Banner


@receiver(pre_delete, sender=Banner)
def delete_banner_files(sender, instance=None, created=False, **kwargs):
    """Banner对象删除前触发"""
    img = getattr(instance, 'img', '')  # <class 'django.db.models.fields.files.ImageFieldFile'>
    img.delete(save=False)
