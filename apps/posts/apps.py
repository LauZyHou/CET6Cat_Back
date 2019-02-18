from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = "帖子管理"

    def ready(self):
        import posts.signals
