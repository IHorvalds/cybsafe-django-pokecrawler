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
    sprites_fk = models.ForeignKey(Sprite, null=True, on_delete=models.SET_NULL)

    @property
    def sprites(self):
        """Get the raw sprite urls without another API call.
        """
        return [
            self.sprites_fk.front_default,
            self.sprites_fk.front_shiny,
            self.sprites_fk.front_female,
            self.sprites_fk.front_shiny_female,
            self.sprites_fk.back_default,
            self.sprites_fk.back_shiny,
            self.sprites_fk.back_female,
            self.sprites_fk.back_shiny_female
        ]