from django.db import models
from django.utils import timezone

class Sprite(models.Model):
    """Sprites of a Pokemon.
    
    Front and back view for normal and shiny types, for both Pokemon genders.
    """
    front_default = models.CharField(max_length=512, null=True)
    front_shiny = models.CharField(max_length=512, null=True)
    front_female = models.CharField(max_length=512, null=True)
    front_shiny_female = models.CharField(max_length=512, null=True)
    back_default = models.CharField(max_length=512, null=True)
    back_shiny = models.CharField(max_length=512, null=True)
    back_female = models.CharField(max_length=512, null=True)
    back_shiny_female = models.CharField(max_length=512, null=True)
    pokemon = models.ForeignKey('Pokemon', on_delete=models.CASCADE)

class Pokemon(models.Model):
    """Pokemon model
    """
    identifier = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False)
    desc = models.TextField(null=True)
    freshness = models.DateTimeField(default=timezone.now)
    species = models.CharField(max_length=256, null=False)
    base_experience = models.IntegerField()
    height = models.IntegerField()

    @property
    def sprites(self):
        """Get the raw sprite urls without another API call.
        """

        sprites = Sprite.objects.filter(pokemon__identifier=self.identifier).latest('id')
        if sprites is not None:
            return {
                "front_default": sprites.front_default,
                "front_shiny": sprites.front_shiny,
                "front_female": sprites.front_female,
                "front_shiny_female": sprites.front_shiny_female,
                "back_default": sprites.back_default,
                "back_shiny": sprites.back_shiny,
                "back_female": sprites.back_female,
                "shiny_female": sprites.back_shiny_female
            }
        else:
            return {
                "front_default": None,
                "front_shiny": None,
                "front_female": None,
                "front_shiny_female": None,
                "back_default": None,
                "back_shiny": None,
                "back_female": None,
                "shiny_female": None
            }
