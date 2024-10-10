from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Tinytalefactory.common'

    def ready(self):
        import Tinytalefactory.common.signals
