from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Pokemon, Sprite

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        Model = User
        fields = ['url', 'username', 'email']

class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokemon
        fields = ['url', 'name', 'desc', 'base_experience', 'height', 'species', 'sprites']

class SpriteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sprite
        fields = ['url', 'front_default', 'front_shiny', 'front_female', 'front_shiny_female', 'back_default', 'back_shiny', 'back_female', 'back_shiny_female', 'pokemon']
