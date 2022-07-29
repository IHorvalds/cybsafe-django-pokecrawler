from datetime import timedelta
from django.utils import timezone
import requests
import logging

from django.conf import settings
from pokecrawler.models import Pokemon

from .utils import createSprite, createTypeList, createPastTypeList

logging.basicConfig(format="%(asctime)s - %(levelname)s %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def findNewPokemon():
    """Look for new Pokemons.
    """
    print("Starting crawler")
    logging.info("Looking for new Pokemon.")
    try:
        lastAdded = Pokemon.objects.latest("identifier").identifier
    except Pokemon.DoesNotExist:
        lastAdded = 0
    for id_offset in range(settings.POKEMON_BATCH_SIZE):
        identifier = lastAdded + 1 + id_offset
        saveNewPokemon(identifier)

def refreshStalePokemon():
    """Check stale Pokemons for updates.
    """

    logging.info("Refreshing stale Pokemons.")
    stalePokemons = Pokemon.objects.filter(freshness__lt=(timezone.now() - timedelta(seconds=settings.STALENESS_THRESHOLD_SECONDS))).all()
    for pokemon in stalePokemons:
        try:
            response = requests.get(f"{settings.POKEAPI_URL}pokemon/{pokemon.identifier}", timeout=5)
            if response.ok:
                jsonResponse = response.json()

                sprite = createSprite(jsonResponse["sprites"])
                
                if pokemon.sprites_fk is not None:
                    pokemon.sprites_fk.delete()
                pokemon.sprites_fk = sprite

                types = createTypeList(jsonResponse["types"])
                pastTypes = createPastTypeList(jsonResponse["past_types"])
                pokemon.name = jsonResponse["name"]
                pokemon.species = jsonResponse["species"]["name"]
                pokemon.height = jsonResponse["height"]
                pokemon.freshness = timezone.now()
                pokemon.desc = f"""\
{jsonResponse["name"]} has types {types}, past types {pastTypes} and has {len(jsonResponse["abilities"])}
"""
                pokemon.save()
            else:
                logging.info(f"Skipping Pokemon with ID {pokemon.identifier} due to exception.")
        except requests.exceptions.Timeout:
            logging.info(f"Timeout for ID {pokemon.identifier}. Moving on...")
        except Exception:
            logging.info(f"Skipping Pokemon with ID {pokemon.identifier} due to exception.")


def saveNewPokemon(identifier):
    try:
        response = requests.get(f"{settings.POKEAPI_URL}pokemon/{identifier}", timeout=5)
        if response.ok:
            jsonResponse = response.json()

            sprite = createSprite(jsonResponse["sprites"])
            types = createTypeList(jsonResponse["types"])
            pastTypes = createPastTypeList(jsonResponse["past_types"])

            newPokemon = Pokemon()
            newPokemon.name = jsonResponse["name"]
            newPokemon.species = jsonResponse["species"]["name"]
            newPokemon.height = jsonResponse["height"]
            newPokemon.base_experience = int(jsonResponse["base_experience"])
            newPokemon.sprites_fk = sprite
                
            newPokemon.desc = f"""\
{jsonResponse["name"]} has types {", ".join(types)}, past types {", ".join(pastTypes)} and has {len(jsonResponse["abilities"])} abilities.\
"""

            newPokemon.save()
        else:
            logging.info(f"Skipping Pokemon with ID {identifier} due to exception.")

    except requests.exceptions.Timeout:
        logging.info(f"Timeout for ID {identifier}. Moving on...")
    except Exception:
        logging.info(f"Skipping Pokemon with ID {identifier} due to exception.")

