from django.db import models


# Create your models here.

class User(models.Model):
    """用户"""
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)
    email = models.EmailField()
    sex = models.NullBooleanField()
    tel = models.CharField(max_length=15)
    cat_b = models.PositiveIntegerField()
    address = models.CharField(max_length=100)
    url = models.URLField()
    birthday = models.DateField()
    school = models.CharField(max_length=40)
    real_score = models.PositiveSmallIntegerField()
    pred_score = models.PositiveSmallIntegerField()
    want_score = models.PositiveSmallIntegerField()
    join_time = models.DateTimeField()
    vip = models.PositiveSmallIntegerField()
