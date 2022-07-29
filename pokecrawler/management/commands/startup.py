from time import sleep
from django.core.management.base import BaseCommand
from django.conf import settings

from pokecrawler.tasks import findNewPokemon, refreshStalePokemon

class Command(BaseCommand):
    def handle(self, **options):
        while True:
            findNewPokemon()
            refreshStalePokemon()
            sleep(settings.RECHECK_INTERVAL_SECONDS)