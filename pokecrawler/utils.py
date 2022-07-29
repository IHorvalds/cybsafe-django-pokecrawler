import logging

from pokecrawler.models import Sprite

logging.basicConfig(format="%(asctime)s - %(levelname)s %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

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

    sprite.save()
    return sprite


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
