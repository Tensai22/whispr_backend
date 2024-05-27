from django.apps import AppConfig


class LogicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logic'


class YourAppConfig(AppConfig):
    name = 'logic'

    def ready(self):
        import logic.signals
