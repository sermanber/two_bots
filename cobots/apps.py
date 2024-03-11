from django.apps import AppConfig


class CobotsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cobots'

    def ready(self):
        import cobots.signals