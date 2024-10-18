from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # Connect the signal to the handler
        post_migrate.connect(load_fixtures, sender=self)

def load_fixtures(sender, **kwargs):
    # Load the fixtures after migrations
    call_command('loaddata', 'main/fixtures/products.json')
