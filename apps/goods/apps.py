from django.apps import AppConfig


class GoodsConfig(AppConfig):
    name = 'goods'
    verbose_name = "商品管理"

    def ready(self):
        import goods.signals
