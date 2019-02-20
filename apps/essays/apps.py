from django.apps import AppConfig


class EssaysConfig(AppConfig):
    name = 'essays'
    verbose_name = "作文管理"

    def ready(self):
        import essays.signals