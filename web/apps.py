from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'

    def ready(self):
        pass


@receiver(post_migrate)
def load_genres(sender, **kwargs):
    # Importamos el modelo Genre aquí para evitar la referencia cruzada
    from .models import Genre

    # Verificamos si el modelo Genre ya existe en la base de datos
    if not Genre.objects.exists():
        call_command('load_genres')

