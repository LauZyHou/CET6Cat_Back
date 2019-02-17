from django.apps import AppConfig


class VideosConfig(AppConfig):
    name = 'videos'
    verbose_name = "视频管理"

    def ready(self):
        import videos.signals
