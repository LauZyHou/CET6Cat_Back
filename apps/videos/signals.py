from django.db.models.signals import pre_delete
from django.dispatch import receiver

from videos.models import Video


@receiver(pre_delete, sender=Video)
def delete_video_files(sender, instance=None, created=False, **kwargs):
    """Video对象删除前触发"""
    video = getattr(instance, 'content', '')  # <class 'django.db.models.fields.files.FieldFile'>
    img = getattr(instance, 'thumb', '')  # <class 'django.db.models.fields.files.ImageFieldFile'>
    # 删除视频和缩略图
    video.delete(save=False)
    img.delete(save=False)
