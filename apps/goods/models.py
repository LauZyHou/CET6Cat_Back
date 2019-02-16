from django.db import models


# Create your models here.

class Goods(models.Model):
    """
    商品Model
    """
    name = models.CharField(max_length=100, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name  # 复数形式

    def __str__(self):  # py3都是unicode的,所以只要指定str就可以
        return self.name
