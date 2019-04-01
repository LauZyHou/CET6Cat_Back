from django.apps import AppConfig


class WordsConfig(AppConfig):
    name = 'words'
    verbose_name = "单词管理"

    def ready(self):
        import words.signals
