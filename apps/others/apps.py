from django.apps import AppConfig


class OthersConfig(AppConfig):
    name = 'others'
    verbose_name = "其它资源管理"

    def ready(self):
        import others.signals
