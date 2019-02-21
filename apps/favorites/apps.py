from django.apps import AppConfig


class FavoritesConfig(AppConfig):
    name = 'favorites'
    verbose_name = "关注&收藏管理"

    def ready(self):
        import favorites.signals
