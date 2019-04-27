from django.db.models.signals import pre_delete
from django.dispatch import receiver

from videos.models import Video
from db_tools.redis_pool import RedisPool


@receiver(pre_delete, sender=Video)
def delete_video_files(sender, instance=None, created=False, **kwargs):
    """Video对象删除前触发"""
    # 删除视频和缩略图
    video = getattr(instance, 'content', '')  # <class 'django.db.models.fields.files.FieldFile'>
    img = getattr(instance, 'thumb', '')  # <class 'django.db.models.fields.files.ImageFieldFile'>
    video.delete(save=False)
    img.delete(save=False)
    # 删除redis中的key
    vid = getattr(instance, 'id', '')
    r = RedisPool.get_connection()
    r.delete("video_" + str(vid))
