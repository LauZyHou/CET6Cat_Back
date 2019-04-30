from django.db.models.signals import pre_delete
from django.dispatch import receiver

from others.models import Banner, Audio, Translate
from db_tools.mongo_pool import CET6CatDB


@receiver(pre_delete, sender=Banner)
def delete_banner_files(sender, instance=None, created=False, **kwargs):
    """Banner对象删除前触发"""
    img = getattr(instance, 'img', '')  # <class 'django.db.models.fields.files.ImageFieldFile'>
    img.delete(save=False)


@receiver(pre_delete, sender=Audio)
def delete_audio_files(sender, instance=None, created=False, **kwargs):
    """Audio对象删除前触发"""
    # <class 'django.db.models.fields.files.FieldFile'>
    content = getattr(instance, 'content', '')
    content.delete(save=False)
    exam = getattr(instance, 'exam', '')
    exam.delete(save=False)
    answer = getattr(instance, 'answer', '')
    answer.delete(save=False)


@receiver(pre_delete, sender=Translate)
def delete_translate_files(sender, instance=None, created=False, **kwargs):
    """Translate对象删除前触发,删除翻译资源文件"""
    # <class 'django.db.models.fields.files.FieldFile'>
    exam = getattr(instance, 'exam', '')
    exam.delete(save=False)
    answer = getattr(instance, 'answer', '')
    answer.delete(save=False)


@receiver(pre_delete, sender=Translate)
def delete_translate_files(sender, instance=None, created=False, **kwargs):
    """Translate对象删除前触发,删除MongoDB中用户对此资源的的翻译"""
    id = getattr(instance, 'id', '')
    CET6CatDB.translate.remove({'tid': id})
