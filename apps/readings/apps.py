from django.apps import AppConfig


class ReadingsConfig(AppConfig):
    name = 'readings'
    verbose_name = "文章管理"

    def ready(self):
        import readings.signals
