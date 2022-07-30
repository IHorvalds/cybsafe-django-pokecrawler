from django.conf import settings
from django.utils import timezone

import requests
import logging
from datetime import timedelta

from .models import Pokemon, Sprite
from pokecrawler.celery import app

logging.basicConfig(format="%(asctime)s - %(levelname)s %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

@app.on_after_finalize.connect
def setupPeriodicTasks(sender, **kwargs):
    ## add task for crawling the api
    sender.add_periodic_task(settings.CRAWL_INTERVAL_SECONDS, findNewPokemons.s(), name="Crawl API for new Pokemons.")

    ## add task for refreshing stale pokemons
    sender.add_periodic_task(settings.REFRESH_INTERVAL_SECONDS, refreshStalePokemons.s(), name="Refresh stale Pokemons.")


@app.task
def findNewPokemons():
    logging.info("Looking for new Pokemon.")
    try:
        lastAdded = Pokemon.objects.latest("identifier").identifier
    except Pokemon.DoesNotExist:
        lastAdded = 0
    
    for id_offset in range(settings.POKEMON_BATCH_SIZE):
        identifier = lastAdded + 1 + id_offset
        logging.info(f"Trying id {identifier}")
        try:
            response = requests.get(f"{settings.POKEAPI_URL}pokemon/{identifier}", timeout=5)
            if response.ok:
                pokemon = Pokemon()
                createPokemonFromObj(pokemon, response.json())
                pokemon.save()
            else:
                logging.error(f"Network exception for new Pokemon with ID {identifier}")
        except requests.exceptions.Timeout:
            logging.error(f"Timeout reached for ID {identifier}")

@app.task
def refreshStalePokemons():
    logging.info("Refreshing stale Pokemons.")
    stalePokemons = Pokemon.objects.filter(freshness__lt=(timezone.now() - timedelta(seconds=settings.STALENESS_THRESHOLD_SECONDS))).all()
    for pokemon in stalePokemons:
        logging.info(f"Updating Pokemon {pokemon.identifier}.")
        try:
            response = requests.get(f"{settings.POKEAPI_URL}pokemon/{pokemon.identifier}", timeout=5)
            if response.ok:
                updatePokemonFromObj(pokemon, response.json())
            else:
                logging.error(f"Network exception for updating Pokemon {pokemon.identifier}")
        except requests.exceptions.Timeout:
            logging.error(f"Timeout reached for updating Pokemon {pokemon.identifier}")

def createPokemonFromObj(pokemon, obj):
    pokemon.name = obj["name"]
    pokemon.species = obj["species"]["name"]
    pokemon.height = obj["height"]
    pokemon.freshness = timezone.now()
    pokemon.base_experience = int(obj["base_experience"])

    types = createTypeList(obj["types"])
    pastTypes = createPastTypeList(obj["past_types"])

    typesString = ""
    if len(types) == 1:
        typesString = f"type {types[0]}"
    elif len(types) > 1:
        typesString = f"types {', '.join(types)}"

    pastTypesString = ""
    if len(pastTypes) == 0:
        pastTypesString = "no past types"
    elif len(pastTypes) == 1:
        pastTypesString = f"past type {pastTypes[0]}"
    elif len(pastTypes) > 1:
        pastTypesString = f"past types {', '.join(pastTypes)}"
    
    pokemon.desc = f"""\
{obj["name"]} has {typesString}, {pastTypesString} and has {len(obj["abilities"])} abilities.
"""
    pokemon.save()

    sprites = createSprite(obj["sprites"])
    sprites.pokemon = pokemon

    sprites.save()

def updatePokemonFromObj(pokemon, obj):
    pokemon.name = obj["name"]
    pokemon.species = obj["species"]["name"]
    pokemon.height = obj["height"]
    pokemon.freshness = timezone.now()
    pokemon.base_experience = int(obj["base_experience"])

    types = createTypeList(obj["types"])
    pastTypes = createPastTypeList(obj["past_types"])

    typesString = ""
    if len(types) == 1:
        typesString = f"type {types[0]}"
    elif len(types) > 1:
        typesString = f"types {', '.join(types)}"

    pastTypesString = ""
    if len(pastTypes) == 0:
        pastTypesString = "no past types"
    elif len(pastTypes) == 1:
        pastTypesString = f"past type {pastTypes[0]}"
    elif len(pastTypes) > 1:
        pastTypesString = f"past types {', '.join(pastTypes)}"
    
    pokemon.desc = f"""\
{obj["name"]} has {typesString}, {pastTypesString} and has {len(obj["abilities"])} abilities.
"""
    pokemon.save()

    sprites = createSprite(obj["sprites"])
    sprites.pokemon = pokemon

    sprites.save()

def createTypeList(obj):
    typeList = []

    for _type in obj:
        typeList.append(_type["type"]["name"])
    return typeList

def createPastTypeList(obj):
    typeList = []

    for _types in obj:
        for __type in _types["types"]:
            typeList.append(__type["type"]["name"])
    return typeList

def createSprite(obj):
    sprite = Sprite()

    sprite.front_default = obj["front_default"]
    sprite.front_shiny = obj["front_shiny"]
    sprite.front_female = obj["front_female"]
    sprite.front_shiny_female = obj["front_shiny_female"]
    sprite.back_default = obj["back_default"]
    sprite.back_shiny = obj["back_shiny"]
    sprite.back_female = obj["back_female"]
    sprite.back_shiny_female = obj["back_shiny_female"]

    return sprite