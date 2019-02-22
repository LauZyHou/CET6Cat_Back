import xadmin
from goods.models import Goods


class GoodsAdmin(object):
    """商品"""
    list_display = ['name', 'click_num', 'sold_num']


xadmin.site.register(Goods, GoodsAdmin)
