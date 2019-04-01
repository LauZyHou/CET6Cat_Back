from django.db import models


# Create your models here.

class Word(models.Model):
    """
    单词Model
    """
    name = models.CharField(max_length=20, verbose_name="名称")
    explain = models.CharField(max_length=50, verbose_name="释义")

    class Meta:
        verbose_name = "单词"
        verbose_name_plural = "单词们"

    def __str__(self):
        return self.name
